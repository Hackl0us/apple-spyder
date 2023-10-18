import logging

import requests
import yaml


def _get_weibo_config():
    with open("res/config.yaml", "r") as stream:
        try:
            config = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
    return config['weibo']


class Weibo:
    def __init__(self):
        config = _get_weibo_config()
        self.enable = config['enable']
        self.access_token = config['access-token']
        self.redirect_uri = config['redirect-uri']
        self.rip = config['rip']

    def post_weibo(self, message):
        if not self.enable:
            logging.warning("Weibo posting feature is DISABLED.")
            return

        url = "https://api.weibo.com/2/statuses/share.json"

        params = {"access_token": self.access_token, "status": str(message) + self.redirect_uri, "rip": self.rip}

        res = requests.post(url, data=params)
        print(res.text)
