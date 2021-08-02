import configparser

from dataclasses import dataclass, asdict


def load_config(path: str):
    config = configparser.ConfigParser()
    config.read(path)
    return asdict(Config(**config['insales']))


def check_hostname(hostname: str):
    if not hostname.startswith('https://'):
        hostname = 'https://%s' % hostname
    if not hostname.endswith('/'):
        hostname += '/'
    return hostname


@dataclass
class Config:
    hostname: str
    apikey: str
    password: str

    def __post_init__(self):
        self.hostname = check_hostname(self.hostname)
