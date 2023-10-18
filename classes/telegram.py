import logging

import requests
import yaml


def _get_bot_config():
    with open("res/config.yaml", "r") as stream:
        try:
            config = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
    return config['telegram']


class Telegram:
    def __init__(self):
        config = _get_bot_config()
        self.enable = config['enable']
        self.bot_token = config['bot-token']
        self.chat_id = config['chat-id']

    def send_message(self, message, chat_id=None, parse_in_markdown=False):
        if not self.enable:
            logging.warning("Telegram posting feature is DISABLED.")
            return

        if chat_id is None:
            chat_id = self.chat_id

        send_message_url = f'https://api.telegram.org/bot{self.bot_token}/sendMessage?chat_id={chat_id}&text={message}'

        if parse_in_markdown:
            send_message_url += '&parse_mode=markdown'

        requests.get(send_message_url)
