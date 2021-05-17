import requests

from abc import ABC, abstractmethod
from functools import cached_property

from .decorators import request


class BaseController:
    __access = None
    headers = {'Content-Type': 'application/json; charset=utf-8'}
    filters = None

    def __new__(cls, *args, **kwargs):
        access = kwargs.pop('access', None)
        if not access and not cls.__access:
            raise NotImplementedError("Config not initialized")
        elif not cls.__access:
            cls.__access = access
        return super().__new__(cls)

    @classmethod
    def register_filters(cls, filters_provider):
        cls.filters = filters_provider

    @cached_property
    def connection_established(self) -> bool:
        url = f'{self.__access}/admin/account.json'
        return requests.get(url, headers=self.headers).ok

    @request
    def _get(self, uri: str) -> requests.Response:
        url = f'{self.__access}/{uri}'
        response = requests.get(url, headers=self.headers)
        return response

    @request
    def _get_all(self, uri: str, **params) -> requests.Response:
        url = f'{self.__access}/{uri}'
        response = requests.get(url, headers=self.headers, params=params)
        return response

    @request
    def _create(self, uri: str, json: dict) -> requests.Response:
        url = f'{self.__access}/{uri}'
        response = requests.post(url, headers=self.headers, json=json)
        return response

    @request
    def _update(self, uri: str, json: dict) -> requests.Response:
        url = f'{self.__access}/{uri}'
        response = requests.put(url, headers=self.headers, json=json)
        return response

    @request
    def _delete(self, uri: str) -> requests.Response:
        url = f'{self.__access}/{uri}'
        response = requests.delete(url, headers=self.headers)
        return response


class IterableMixin(ABC):

    @abstractmethod
    def __iter__(self):
        pass

    @abstractmethod
    def __call__(self, *args, **kwargs):
        pass
