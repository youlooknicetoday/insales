from datetime import datetime
from typing import Optional, Union

from ..src.endpoints import BaseController, IterableMixin
from ..src.exceptions import DataNotProvided


def register_builders():
    factory = CollectControllerFactory()
    factory.register_builder('ProductsController', ProductsFilter())
    factory.register_builder('CollectionsController', CollectionsFilter)


class CollectControllerFactory:

    def __init__(self):
        self._builders = {}

    def register_builder(self, key, builder):
        self._builders[key] = builder

    def create(self, key, **kwargs):
        builder = self._builders.get(key)
        if not builder:
            raise ValueError(key)
        return builder(**kwargs)


class FilterProvider(CollectControllerFactory):

    def get(self, caller_name):
        return self.create(caller_name)


class ProductsFilter(BaseController, IterableMixin):

    def get_all(self):
        uri = 'admin/collects.json'
        products = self._get_all(uri, category_id=self.category_id).json()
        return products

    def __iter__(self):
        for product in self.get_all():
            yield product['id']

    def __call__(self, /, category_id: int):
        self.category_id = category_id
        return self


class CollectionsFilter(BaseController, IterableMixin):

    def __init__(self, product_id):
        self.product_id = product_id

    def get_collector(self, category_id, product_id):
        if not category_id and not product_id:
            raise DataNotProvided

    def __iter__(self):
        pass

    def __call__(self, *args, **kwargs):
        pass



