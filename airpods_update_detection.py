import logging
import plistlib
import urllib.request

from classes.database import DatabaseUtil
from classes.datetime import covert_to_local_timezone
from classes.datetime import is_a_previous_time
from classes.telegram import Telegram
from classes.weibo import Weibo


def main():
    ota_update_url = "https://mesu.apple.com/assets/com_apple_MobileAsset_UARP_A2618/com_apple_MobileAsset_UARP_A2618.xml"

    with urllib.request.urlopen(ota_update_url) as response:
        firmware_release_date = response.headers['last-modified']
        plist_content = plistlib.loads(response.read())

    # Get last OTA update time from db
    db = DatabaseUtil()
    last_update_time = db.db_select("SELECT update_time FROM accessory_ota_update WHERE model = 'A2618'")[0][0]

    if not last_update_time:
        last_update_time = "Thu, 01 Jan 1970 00:00:00 UTC"
        logging.warning("last_update_time is empty in database, set timestamp to: " + last_update_time)

    # Check if OTA is up-to-date
    if last_update_time == firmware_release_date:
        return

    # Parse OTA update plist
    asset = plist_content["Assets"][0]

    firmware_version = f"{asset['FirmwareVersionMajor']}.{asset['FirmwareVersionMinor']}.{asset['FirmwareVersionRelease']}"
    firmware_build = asset["Build"]
    firmware_download_size = asset["_DownloadSize"] / 1024 / 1024
    # firmware_url = asset["__BaseURL"] + asset["__RelativePath"]

    # Construct notification message
    if is_a_previous_time(last_update_time, firmware_release_date):
        message = f'''📤 Apple 为 *AirPods Pro 2* 发布新固件\n
        🌀 编译版本：*{firmware_build}*
        🔢 版本号：*{firmware_version}*
        📦 固件大小：*{firmware_download_size:.2f}* MB
        🕐 发布时间: *{covert_to_local_timezone(firmware_release_date).strftime('%Y/%m/%d %H:%M:%S')}*'''
    else:
        message = f"🙊Apple *撤回* AirPods Pro 2 固件更新至 *{firmware_version}({firmware_build})*"

    logging.info(message)

    # Post message
    telegram = Telegram()
    telegram.send_message(message, parse_in_markdown=True)

    weibo = Weibo()
    weibo.post_weibo(message.replace('*', ''))

    # Update record
    db.db_operate("UPDATE accessory_ota_update SET update_time = ? WHERE model = 'A2618'", (firmware_release_date,))
    logging.info("Update feed publish time in database: " + firmware_release_date)


if __name__ == "__main__":
    main()
