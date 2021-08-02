import logging
from abc import ABC, abstractmethod

from ..config import load_config


class BaseClient(ABC):
    __logger = logging.getLogger(__name__)

    def __init__(self, /, hostname, apikey, password):
        self.session_data = {
            'base_url': hostname,
            'auth': (apikey, password),
            'headers': {
                'Content-Type': 'application/json; charset=utf-8',
                'User-Agent': 'python-httpx/insalesapi',
            },
            'event_hooks': {
                'response': [self.log_response]
            }
        }
        self._session = None

    @abstractmethod
    def request(self, method, url, *, result_type=None, json=None, params=None):
        pass

    @abstractmethod
    def close(self):
        pass

    @abstractmethod
    def log_response(self, response):
        pass

    @classmethod
    def from_config(cls, path):
        config = load_config(path)
        return cls(**config)



