import configparser

from dataclasses import dataclass
from pathlib import Path


@dataclass
class Config:
    hostname: str
    apikey: str
    password: str

    def __iter__(self):
        yield self.hostname
        yield self.apikey
        yield self.password


def load_config(path):
    config = configparser.ConfigParser()
    config.read(path)
    return Config(**config['insales'])
