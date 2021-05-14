from .endpoints import BaseController, IterableMixin
from ..products.endpoints import ProductsController


def register_filters():
    factory = FiltersProvider()
    factory.register_builder(ProductsController, ProductsFilter)
    # factory.register_builder(CollectionsController, CollectionsFilter)
    return factory


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


class FiltersProvider(CollectControllerFactory):

    def get(self, key, **kwargs):
        return self.create(key, **kwargs)


class ProductsFilter(BaseController, IterableMixin):

    def get_all(self):
        uri = 'admin/collects.json'
        products = self._get_all(uri, collection_id=self.collection_id).json()
        return products

    def __iter__(self):
        for product in self.get_all():
            yield product

    def __call__(self, /, collection_id: int, *args, **kwargs):
        self.collection_id = collection_id
        print(self.collection_id)
        return self


class CollectionsFilter(BaseController, IterableMixin):

    def get_all(self):
        uri = 'admin/collects.json'
        collections = self._get_all(uri, product_id=self.product_id).json()
        return collections

    def __iter__(self):
        pass

    def __call__(self, /, product_id, *args, **kwargs):
        self.product_id = product_id
        return self
