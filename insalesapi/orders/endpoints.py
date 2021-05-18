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

    def get(self, /, order_id: Union[int, str]) -> dict:
        uri = f'admin/orders/{order_id}.json'
        order = self._get(uri).json()
        return order

    @property
    def count(self) -> int:
        uri = 'admin/orders/count.json'
        result = self._get(uri).json()
        return result['count']
