from typing import Iterator

from ..src.endpoints import BaseController, IterableMixin


class CollectionsFilter(BaseController, IterableMixin):

    def get_all(self):
        uri = 'admin/collects.json'
        collections = self._get_all(uri, product_id=self.product_id).json()
        return collections

    def __iter__(self) -> Iterator[str]:
        for item in self.get_all():
            yield item['collection_id']

    def __call__(self, /, product_id: int, *args, **kwargs):
        self.product_id = product_id
        return self
