import logging

from httpx import Client
from .base_client import BaseClient
from .endpoints import EndpointsMixin


class InSalesClient(BaseClient, EndpointsMixin):
    __logger = logging.getLogger(__name__)

    def __init__(self, /, hostname, apikey, password):
        super().__init__(hostname=hostname, apikey=apikey, password=password)
        self._session = Client(**self.session_data)
        del self.session_data

    def close(self):
        self._session.close()

    def log_response(self, response):
        self.__logger.debug(
            'Status code: %d, Runtime: %s ms, Usage limit: %s',
            response.status_code, response.headers['x-runtime'], response.headers['api-usage-limit']
        )

    def request(
            self, method, url, *,
            result_type=None, many=False, json=None, params=None,
    ):
        response = self._session.request(
            method=method,
            url=url,
            json=json,
            params=params,
        )
        if result_type is not None:
            if many:
                return [result_type(**data) for data in response.json()]
            return result_type(**response.json())
        return response.json()
