from datetime import datetime
from typing import Optional, Union

from ..schemas.products import Product
from .base import BaseController


class ProductsController(BaseController):

    def get_product(self, /, product_id: Union[int, str]) -> Product:
        uri = f'admin/products/{product_id}.json'
        return self._request('GET', uri, result_type=Product)

    def get_products(
            self, *,
            page: Optional[Union[int, str]] = None,
            per_page: Optional[Union[int, str]] = None,
            updated_since: Optional[Union[datetime, str]] = None,
            from_id: Optional[Union[int, str]] = None,
            with_deleted: Optional[bool] = None,
            deleted: Optional[bool] = None
    ) -> list[Product]:
        uri = 'admin/products.json'
        params = {
            'page': page, 'per_page': per_page,
            'updated_since': updated_since, 'from_id': from_id,
            'with_deleted': with_deleted, 'deleted': deleted,
        }
        params = self._exclude_none(params)
        return self._request('GET', uri, result_type=Product, many=True, params=params)

    def get_products_count(self) -> dict[str, int]:
        uri = 'admin/products/count.json'
        return self._request('GET', uri)
