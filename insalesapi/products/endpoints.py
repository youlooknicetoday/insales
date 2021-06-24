import logging

from datetime import datetime
from fastapi.encoders import jsonable_encoder
from typing import Optional, Union, Iterator

from .related import RelatedProducts
from .schemas import Products, Product
from ..src.endpoints import BaseController, IterableMixin
from ..src.exceptions import WrongPageNumber

logger = logging.getLogger(__name__)


class ProductsController(BaseController, IterableMixin):

    def __init__(self, api):
        super().__init__(api)
        # self.where = self._filters.get(self.__class__)
        self.related = RelatedProducts(self.api)

    def get_all(
            self, /,
            page: Optional[Union[int, str]] = None,
            per_page: Optional[Union[int, str]] = None,
            updated_since: Optional[Union[datetime, str]] = None,
            from_id: Optional[Union[int, str]] = None,
            with_deleted: Optional[bool] = None,
            deleted: Optional[bool] = None
    ) -> list[Product]:
        uri = 'admin/products.json'
        if per_page and not 10 <= per_page <= 250:
            logger.info('%s', 'Per page param have to be greater or equal 10 and less or equal 250')
        products_list = self._get_all(
            uri, page=page, per_page=per_page, updated_since=updated_since, from_id=from_id,
            with_deleted=with_deleted, deleted=deleted).json()
        return Products(list=products_list).list

    def get(self, /, product_id: Union[int, str]) -> Product:
        uri = f'admin/products/{product_id}.json'
        product = self._get(uri).json()
        return Product(**product)

    @property
    def count(self) -> int:
        uri = 'admin/products/count.json'
        result = self._get(uri).json()
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
        uri = 'admin/products.json'
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
        product = self._create(uri, product_json).json()
        return Product(**product)

    def delete(self, /, product_id: Union[int, str]):
        uri = f'admin/products/{product_id}.json'
        response = self._delete(uri)
        return 'ok' in response.json().values()

    def update(
            self, /,
            product_id: Union[int, str],
            title: Optional[str] = None, sku: Optional[Union[int, str]] = None,
            quantity: Optional[int] = None, price: Optional[Union[int, str]] = None,
            description: Optional[str] = None, short_description: Optional[str] = None,
            **extra_fields
    ) -> Product:
        uri = f'admin/products/{product_id}.json'
        product_json = jsonable_encoder({
            'product': {
                'title': title,
                'sku': sku,
                'quantity': quantity,
                'price': price,
                'description': description,
                'short_description': short_description,
                **extra_fields
            }}, exclude_none=True)
        product = self._update(uri, product_json).json()
        return Product(**product)

    def __iter__(self) -> Iterator[Product]:
        for page in self.page_range:
            products = self.get_all(page, self.per_page)
            for product in products:
                yield product

    def __call__(self, /, start_page: int = 1, end_page: Optional[int] = None, per_page: int = 100):
        if not start_page > 0:
            raise WrongPageNumber('Start page must be greater than zero')
        self.per_page = per_page
        end_page = end_page or self.count // self.per_page
        self.page_range = range(start_page, end_page)
        return self
