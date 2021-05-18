from ..collections.endpoints import CollectionsController
from ..collections.filters import CollectionsFilter
from ..products.endpoints import ProductsController
from ..products.filters import ProductsFilter


def register_filters():
    factory = FiltersProvider()
    factory.register_builder(ProductsController, ProductsFilter)
    factory.register_builder(CollectionsController, CollectionsFilter)
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
