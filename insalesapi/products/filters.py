from typing import Iterator

from ..src.endpoints import BaseController, IterableMixin


class ProductsFilter(BaseController, IterableMixin):

    def get_all(self):
        uri = 'admin/collects.json'
        products = self._get_all(uri, collection_id=self.collection_id).json()
        return products

    @property
    def count(self):
        uri = f'admin/products/count.json?collection_id={self.collection_id}'
        result = self._get(uri).json()
        return result['count']

    def __iter__(self) -> Iterator[str]:
        for item in self.get_all():
            yield item['product_id']

    def __call__(self, /, collection_id: int, *args, **kwargs):
        self.collection_id = collection_id
        return self
