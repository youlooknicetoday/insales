import logging

from datetime import datetime
from fastapi.encoders import jsonable_encoder
from typing import Optional, Union

from ..src.endpoints import BaseController

logger = logging.getLogger(__name__)


class OrdersController(BaseController):

    def get_all(
            self, /,
            page: Optional[Union[int, str]] = None,
            per_page: Optional[Union[int, str]] = None,
            updated_since: Optional[Union[datetime, str]] = None,
            from_id: Optional[Union[int, str]] = None,
            fulfillment_status: Optional[list[str]] = None,
            delivery_variant: Optional[list[str]] = None,
            payment_gateway_id: Optional[list[Union[int, str]]] = None
    ) -> dict:
        uri = 'admin/orders.json'
        if per_page and not 10 <= per_page <= 250:
            logger.info('%s', 'Per page param have to be greater or equal 10 and less or equal 250')
        orders_list = self._get_all(
            uri, page=page, per_page=per_page, updated_since=updated_since, from_id=from_id,
            fulfillment_status=fulfillment_status, delivery_variant=delivery_variant,
            payment_gateway_id=payment_gateway_id).json()
        return orders_list

    @property
    def count(self) -> int:
        uri = 'admin/orders/count.json'
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
    ) -> dict:
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
            category_id: Union[int, str],
            title: str, sku: Union[int, str], quantity: int, price: Union[int, str],
            description: Optional[str] = None, short_description: Optional[str] = None,
            sort_weight: Optional[Union[int, float]] = None,
            ignore_discounts: int = 1, vat: int = -1,
            product_field_values_attributes: Optional[list[dict[str, Union[int, str]]]] = None
    ) -> Product:
        pass
