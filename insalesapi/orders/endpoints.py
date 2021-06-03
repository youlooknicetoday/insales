import logging

from datetime import datetime
from fastapi.encoders import jsonable_encoder
from typing import Optional, Union

from .schemas import Order, Orders
from ..src.endpoints import BaseController
from ..src.exceptions import WrongPageNumber

logger = logging.getLogger(__name__)


def prepare(**fields):
    """
    Function for formatting params in orders
    If you would like to get orders with many statuses like
    fulfillment_status=["new", "delivered"]
    url have to be like this: /admin/orders.json?fulfillment_status[]=new&fulfillment_status[]=delivered
    :param fields: dict[str, str]
    :return: dict[str, str] formatted fields for url param
    """
    tmp = fields.copy()
    for key in tmp.keys():
        fields[f'{key}[]'] = fields.pop(key)
    return fields


class OrdersController(BaseController):

    def get_all(
            self, /,
            page: Optional[Union[int, str]] = None,
            per_page: Optional[Union[int, str]] = None,
            updated_since: Optional[Union[datetime, str]] = None,
            from_id: Optional[Union[int, str]] = None,
            fulfillment_status: Optional[list[str]] = None,
            delivery_variant: Optional[list[str]] = None,
            payment_gateway_id: Optional[list[Union[int, str]]] = None,
            **extra_fields
    ) -> list[Order]:
        uri = 'admin/orders.json'
        if per_page and not 10 <= per_page <= 250:
            logger.info('%s', 'Per page param have to be greater or equal 10 and less or equal 250')
        prepared_fields = prepare(
            fulfillment_status=fulfillment_status, delivery_variant=delivery_variant,
            payment_gateway_id=payment_gateway_id)
        orders_list = self._get_all(uri, page=page, per_page=per_page, updated_since=updated_since, from_id=from_id,
                                    **prepared_fields).json()
        return Orders(list=orders_list).list

    def get(self, /, order_id: Union[int, str]) -> Order:
        uri = f'admin/orders/{order_id}.json'
        order = self._get(uri).json()
        return Order(**order)

    @property
    def count(self) -> int:
        uri = 'admin/orders/count.json'
        result = self._get(uri).json()
        return result['count']

    def __iter__(self):
        for page in self.page_range:
            orders = self.get_all(page, self.per_page)
            for order in orders:
                yield order

    def __call__(self, /, start_page: int = 1, end_page: Optional[int] = None, per_page: int = 100):
        if not start_page > 0:
            raise WrongPageNumber('Start page must be greater than zero')
        self.per_page = per_page
        end_page = end_page or self.count // self.per_page + 2
        self.page_range = range(start_page, end_page)
        return self
