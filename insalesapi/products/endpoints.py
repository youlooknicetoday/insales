import requests

from datetime import datetime
from fastapi.encoders import jsonable_encoder
from typing import Optional, Union

from .schemas import Products, Product
from ..src import Endpoint, logger
from ..src.decorators import request


class ProductsController(Endpoint):

    @request
    def _get_all(self, **params) -> requests.Response:
        url = f'{self.access}/admin/products.json'
        response = requests.get(url, params=params)
        return response

    def get_all(
            self, /,
            updated_since: Optional[Union[datetime, str]] = None,
            from_id: Optional[Union[int, str]] = None,
            page: Optional[Union[int, str]] = None,
            per_page: Optional[Union[int, str]] = None,
            with_deleted: Optional[bool] = None,
            deleted: Optional[bool] = None
    ) -> Products:
        if per_page and not 10 <= per_page <= 250:
            logger.info('%s', 'Per page param have to be greater or equal 10 and less or equal 250')
        products_list = self._get_all(
            updated_since=updated_since, from_id=from_id,
            page=page, per_page=per_page,
            with_deleted=with_deleted, deleted=deleted).json()
        return Products(list=products_list)

    @request
    def _get(self, product_id: Union[int, str]) -> requests.Response:
        url = f'{self.access}/admin/products/{product_id}.json'
        response = requests.get(url)
        return response

    def get(self, /, product_id: Union[int, str]) -> Product:
        uri = f'/admin/products/{product_id}.json'
        product = self._get(product_id).json()
        return Product(**product)

    @request
    def _count(self) -> requests.Response:
        url = f'{self.access}/admin/products/count.json'
        response = requests.get(url)
        return response

    @property
    def count(self) -> int:
        result = self._count().json()
        return result['count']

    def create(
            self, /,
            category_id: Union[int, str],
            title: str, sku: Union[int, str], quantity: int, price: Union[int, str],
            description: Optional[str] = None, short_description: Optional[str] = None,
            sort_weight: Optional[Union[int, float]] = None,
            ignore_discounts: int = 1, vat: int = -1,
            product_field_values_attributes: Optional[list[dict[str, Union[int, str]]]] = None
    ) -> Product:
        uri = '/admin/products.json'
        variants_attributes: list[dict[str, Union[int, str]]] = [{'sku': sku, 'quantity': quantity, 'price': price}]
        product_json = jsonable_encoder({
            'product': {
                'category_id': category_id,
                'title': title,
                'variants_attributes': variants_attributes,
                'ignore_discounts': ignore_discounts,
                'vat': vat,
                'description': description,
                'short_description': short_description,
                'sort_weight': sort_weight,
                'product_field_values_attributes': product_field_values_attributes
            }}, exclude_none=True)
        product = self._create(product_json).json()
        return Product(**product)
