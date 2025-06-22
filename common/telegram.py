import os

import requests
from loguru import logger


def is_telegram_enabled():
    return os.getenv("TELEGRAM_ENABLED", "false").lower() == "true"


class Telegram:
    def __init__(self):
        self.enabled = is_telegram_enabled()
        self.bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
        self.chat_id = os.getenv("TELEGRAM_CHAT_ID")

        if self.enabled:
            if not self.bot_token or not self.chat_id:
                logger.error("Telegram is enabled but bot token or chat ID is not set.")
                self.enabled = False

    def send_message(self, message: str, chat_id: str = None, parse_in_markdown: bool = False):
        if not self.enabled:
            logger.info("Telegram is disabled. Skipping message.")
            return

        chat_id = chat_id or self.chat_id
        url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
        params = {"chat_id": chat_id, "text": message, }

        if parse_in_markdown:
            params["parse_mode"] = "Markdown"

        try:
            response = requests.get(url, params=params, timeout=10)
            if response.status_code != 200:
                logger.error(f"Telegram message failed: {response.status_code} - {response.text}")
            else:
                logger.success("Telegram message sent successfully.")
        except Exception as e:
            logger.exception(f"Telegram send_message error: {e}")
