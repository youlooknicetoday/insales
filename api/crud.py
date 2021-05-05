from abc import ABC
from .src import API


class Base(ABC):

    def __init__(self, api: API):
        self.api = api
