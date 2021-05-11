import configparser
from dataclasses import dataclass
from typing import Union
from pathlib import Path


def init_credentials(path: Union[str, Path]):
    config = configparser.ConfigParser()
    config.read(path)
    API(**config['insales'])


class Endpoint:
    access = None
    headers = {"Content-Type": "application/xml"}

    def __new__(cls, *args, **kwargs):
        api: API = kwargs.pop('api', None)
        if not api and not cls.access:
            raise NotImplementedError("Config not initialized")
        elif not cls.access:
            cls.access = api
        instance = object.__new__(cls)
        return instance


@dataclass
class API:

    apikey: str
    password: str
    hostname: str
    initialized: bool = False

    def __post_init__(self):
        if not self.initialized:
            Endpoint(api=self)
            self.initialized = True

    def __str__(self):
        return "http://{self.apikey}:{self.password}@{self.hostname}".format(self=self)
