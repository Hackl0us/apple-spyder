import logging
import re

import feedparser
import yaml

from classes.database import DatabaseUtil
from classes.datetime import is_a_previous_time
from classes.telegram import Telegram
from classes.weibo import Weibo


def main():
    # Read RSS feed from config
    with open("res/config.yaml", "r") as stream:
        try:
            config = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            logging.error(exc)

    # Parse RSS
    rss_feed = feedparser.parse(config['url']['apple-developer-rss'])
    feed_publish_time = rss_feed.feed.updated
    logging.info("Feed Update time:" + feed_publish_time)

    # Get last feed update time from db
    db = DatabaseUtil()
    last_feed_update_time = \
        db.db_select("SELECT update_time FROM apple_developer_rss WHERE id = 'RSS_FEED_UPDATE_TIME'")[0][0]
    if not last_feed_update_time:
        last_feed_update_time = "Thu, 01 Jan 1970 00:00:00 PDT"
        logging.warning("last_feed_update_time is empty in database, set timestamp to: " + last_feed_update_time)

    # Create empty lists for saving different type release info
    beta_release = []
    prod_release = []

    software_release_keywords = ["iOS", "iPadOS", "watchOS", "tvOS", "macOS", "Xcode"]
    beta_keywords = ["RC", "Release Candidate", "beta"]

    software_release_pattern = r'\b(' + '|'.join(software_release_keywords) + r')\b'
    beta_release_pattern = r'\b(' + '|'.join(beta_keywords) + r')\b'

    if last_feed_update_time != feed_publish_time:
        for entry in rss_feed.entries:
            if is_a_previous_time(last_feed_update_time, entry.published):
                if bool(re.search(software_release_pattern, entry.title)):
                    if bool(re.search(beta_release_pattern, entry.title)):
                        beta_release.append(entry.title)
                        logging.info("Append a BETA release item: " + entry.title)
                    else:
                        prod_release.append(entry.title)
                        logging.info("Append a PROD release item: " + entry.title)
            else:
                continue

    beta_release_message = "🧪 Apple 发布 [测试版] 软件更新\n\n * " + "\n * ".join(beta_release)
    prod_release_message = "📲 Apple 发布 [正式版] 软件更新\n\n * " + "\n * ".join(prod_release)

    telegram = Telegram()
    weibo = Weibo()

    if len(beta_release) > 0:
        logging.info(beta_release_message)
        telegram.send_message(beta_release_message)
        weibo.post_weibo(beta_release_message)

    if len(prod_release) > 0:
        logging.info(prod_release_message)
        telegram.send_message(prod_release_message)
        weibo.post_weibo(prod_release_message)

    # Update record
    db.db_operate("UPDATE apple_developer_rss SET update_time = ? WHERE id = 'RSS_FEED_UPDATE_TIME'",
                  (feed_publish_time,))
    logging.info("Update feed publish time in database: " + feed_publish_time)


if __name__ == "__main__":
    main()
