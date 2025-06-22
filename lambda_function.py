import hashlib
import os
import re
import time
from datetime import datetime, timezone, timedelta

import boto3
import feedparser
import requests
from loguru import logger

from common.telegram import Telegram
from common.weibo import Weibo

# --- Configurations ---
DDB_TABLE_NAME = "apple_software_release"
RSS_FEED_URL = os.getenv("RSS_FEED_URL", "https://developer.apple.com/news/releases/rss/releases.rss")
CUTOFF_DAYS = int(os.getenv("CUTOFF_DAYS", 7))

platform_keywords = ["iOS", "iPadOS", "watchOS", "tvOS", "macOS", "visionOS", "Xcode", "AirPods Firmware"]
beta_keywords = ["RC", "Release Candidate", "beta"]

# --- Initialization ---
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(DDB_TABLE_NAME)


def hash_content(content):
    return hashlib.md5(content.encode()).hexdigest()


def parse_feed(feed_url):
    return feedparser.parse(feed_url, request_headers={"Cache-Control": "no-cache"})


def classify_software_release(item_title):
    platform_pattern = "|".join(re.escape(p) for p in platform_keywords)
    beta_pattern = "|".join(re.escape(k) for k in beta_keywords)

    regex = re.compile(
        rf"\b(?P<platform>{platform_pattern})\s+(?P<version>\d*(?:\.\d+)*)(?:\s*(?P<channel>{beta_pattern}))?",
        re.IGNORECASE, )

    match = regex.search(item_title)
    if not match:
        return "", ""

    platform = match.group("platform")
    major_version = match.group("version").split(".")[0]
    channel = match.group("channel")
    channel = "beta" if channel else "stable"

    return f"{platform} {major_version}".strip(), channel


def get_last_feed_hash():
    response = table.get_item(Key={"platform": "RSS", "channel": "rss"})
    item = response.get("Item")
    if not item:
        return ""
    return item["hash"]


def get_software_build(platform, channel):
    response = table.get_item(Key={"platform": platform, "channel": channel})
    item = response.get("Item")
    if not item:
        return ""
    return item["build"].strip()


def is_recent_release(item_publish_time, feed_update_time, cut_off_days):
    if not item_publish_time or not feed_update_time:
        return False
    feed_update_datetime = datetime.fromtimestamp(time.mktime(feed_update_time))
    item_publish_datetime = datetime.fromtimestamp(time.mktime(item_publish_time))

    if cut_off_days == 0:
        return item_publish_datetime == feed_update_datetime
    else:
        cutoff_datetime = feed_update_datetime - timedelta(days=cut_off_days)
        return cutoff_datetime <= item_publish_datetime


def convert_to_beijing_time(struct_time):
    # Convert struct_time to a UTC timestamp
    utc_timestamp = time.mktime(struct_time)

    # Convert to Beijing time
    beijing_tz = timezone(timedelta(hours=8))
    beijing_time = datetime.fromtimestamp(utc_timestamp, tz=beijing_tz)

    return beijing_time.strftime("%Y 年 %m 月 %d 日 %H:%M:%S")


def lambda_handler(event=None, context=None):
    # 1. Fetch RSS Feed content
    response = requests.get(RSS_FEED_URL)
    rss_feed_content = response.text

    # 2. Hash the content and compare with old hash values
    last_feed_content_hash = get_last_feed_hash()
    current_feed_content_hash = hash_content(rss_feed_content)

    if current_feed_content_hash == last_feed_content_hash:
        logger.info("RSS Feed is up-to-date.")
        return {"status": "no_update"}

    # 3. Parse RSS feed and filter out information
    beta_release = []
    stable_release = []
    updates_to_db = []

    feed = parse_feed(RSS_FEED_URL)
    feed_update_time = feed.feed.updated_parsed

    for entry in feed.entries:
        if not is_recent_release(entry.published_parsed, feed_update_time, CUTOFF_DAYS):
            continue

        platform_major_ver, channel = classify_software_release(entry.title)
        if platform_major_ver == "":
            continue

        old_software_build = get_software_build(platform_major_ver, channel)

        if old_software_build.lower() == entry.title.lower():
            logger.info(f"{platform_major_ver} {channel} has no updates.")
            continue

        if channel == "beta":
            beta_release.append(entry.title)
            logger.info("Append a BETA release item: " + entry.title)

        if channel == "stable":
            stable_release.append(entry.title)
            logger.info("Append a STABLE release item: " + entry.title)

        updates_to_db.append(
            {"platform": platform_major_ver, "channel": channel, "build": entry.title, "release_time": entry.updated, })

    beta_release_message = "🧪 Apple 发布 [测试版] 软件更新\n\n * " + "\n * ".join(beta_release)
    stable_release_message = "📲 Apple 发布 [正式版] 软件更新\n\n * " + "\n * ".join(stable_release)

    telegram = Telegram()
    weibo = Weibo()

    if len(beta_release) > 0:
        logger.info(beta_release_message)
        telegram.send_message(beta_release_message)
        weibo.post_weibo(beta_release_message)

    if len(stable_release) > 0:
        logger.info(stable_release_message)
        telegram.send_message(stable_release_message)
        weibo.post_weibo(stable_release_message)

    # Update software release records
    for update in updates_to_db:
        table.put_item(Item={"platform": update["platform"], "channel": update["channel"], "build": update["build"],
                             "release_time": update["release_time"], })
    # Update RSS feed information
    table.put_item(Item={"platform": "RSS", "channel": "rss", "hash": current_feed_content_hash,
                         "release_time": feed.feed.updated, })

    return {"status": "ok", "updated": len(updates_to_db)}


if __name__ == "__main__":
    lambda_handler(event=None, context=None)
