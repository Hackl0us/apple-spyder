import os

import requests
from loguru import logger


def is_weibo_enabled():
    return os.getenv("WEIBO_ENABLED", "false").lower() == "true"


class Weibo:
    def __init__(self):
        self.enabled = is_weibo_enabled()
        self.access_token = os.getenv("WEIBO_ACCESS_TOKEN")
        self.redirect_uri = os.getenv("WEIBO_REDIRECT_URI")
        self.rip = os.getenv("WEIBO_RIP")

        if self.enabled:
            if not self.access_token:
                logger.error("Weibo is enabled but access token is not set.")
                self.enabled = False

    def post_weibo(self, message: str):
        if not self.enabled:
            logger.info("Weibo is disabled. Skipping post.")
            return

        url = "https://api.weibo.com/2/statuses/share.json"
        params = {"access_token": self.access_token, "status": str(message) + " " + self.redirect_uri, "rip": self.rip}

        try:
            response = requests.post(url, data=params, timeout=10)
            if response.status_code != 200:
                logger.error(f"Weibo post failed: {response.status_code} - {response.text}")
            else:
                logger.success("Weibo post sent successfully.")
        except Exception as e:
            logger.exception(f"Weibo post_weibo error: {e}")
