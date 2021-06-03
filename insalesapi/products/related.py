from fastapi.encoders import jsonable_encoder
from typing import Iterator

from ..src.endpoints import BaseController, IterableMixin


class RelatedProducts(BaseController, IterableMixin):

    def get_all(self, /, product_id: int) -> list[dict[str, int]]:
        uri = f'/admin/products/{product_id}/supplementaries.json'
        related_products_ids = self._get_all(uri).json()
        return related_products_ids

    def create(self, /, product_id: int, related_products_ids: list[int]) -> bool:
        uri = f'/admin/products/{product_id}/supplementaries.json'
        product_json = jsonable_encoder({
            'supplementary_ids': related_products_ids
        })
        response = self._create(uri, product_json)
        return 'ok' in response.json().values()

    def delete(self, /, product_id: int, related_product_id: int) -> bool:
        uri = f'/admin/products/{product_id}/supplementaries/{related_product_id}.json'
        response = self._delete(uri)
        return 'ok' in response.json().values()

    def __iter__(self) -> Iterator[str]:
        for item in self.get_all(self.product_id):
            yield item['id']

    def __call__(self, /, product_id: int, *args, **kwargs):
        self.product_id = product_id
        return self
