import configparser
from typing import Union
from pathlib import Path


def load_config(path: Union[str, Path]):
    config = configparser.ConfigParser()
    config.read(path)
    return API(**config['insales'])


class API:
    headers = {"Content-Type": "application/xml"}

    def __init__(self, apikey, password, hostname):
        self.apikey = apikey
        self.password = password
        self.hostname = hostname

    def __str__(self):
        return "http://{self.apikey}:{self.password}@{self.hostname}".format(self=self)
