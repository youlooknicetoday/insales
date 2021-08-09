from datetime import datetime
from typing import Optional, Union

from ..schemas.orders import Order
from .base import BaseController


def prepare(**fields):
    """
    Function for formatting params in orders
    If you would like to get orders with many statuses like
    fulfillment_status=["new", "delivered"]
    url have to be like this: /admin/orders.json?fulfillment_status[]=new&fulfillment_status[]=delivered
    :param fields: dict[str, str]
    :return: dict[str, str] formatted fields for url param

    >>> prepare(payment_gateway_id=["1", "3"])
    {'payment_gateway_id[]': ['1', '3']}
    """
    tmp = fields.copy()
    for key in tmp.keys():
        fields[f'{key}[]'] = fields.pop(key)
    return fields


class OrdersController(BaseController):

    def get_order(self, /, order_id: Union[int, str]) -> Order:
        uri = f'admin/orders/{order_id}.json'
        return self._request('GET', uri, result_type=Order)

    def get_orders(
            self, *,
            fulfillment_status: list[str] = None,
            delivery_variant: list[Union[int, str]] = None,
            payment_gateway_id: list[Union[int, str]] = None,
            page: Optional[Union[int, str]] = None,
            per_page: Optional[Union[int, str]] = None,
            updated_since: Optional[Union[datetime, str]] = None,
            from_id: Optional[Union[int, str]] = None,
            with_deleted: Optional[bool] = None,
            deleted: Optional[bool] = None,
            **extra_fields
    ) -> list[Order]:
        uri = 'admin/orders.json'
        prepared_fields = prepare(
            fulfillment_status=fulfillment_status,
            delivery_variant=delivery_variant,
            payment_gateway_id=payment_gateway_id
        )
        params = {
            'page': page, 'per_page': per_page,
            'updated_since': updated_since, 'from_id': from_id,
            'with_deleted': with_deleted, 'deleted': deleted,
            **prepared_fields, **extra_fields
        }
        params = self._exclude_none(params)
        return self._request('GET', uri, result_type=Order, many=True, params=params)

    def get_orders_count(self) -> dict[str, int]:
        uri = 'admin/orders/count.json'
        return self._request('GET', uri)
