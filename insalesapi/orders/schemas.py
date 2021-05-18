from datetime import datetime
from pydantic import BaseModel, HttpUrl
from typing import Optional, Union


class FieldValue(BaseModel):
    id: int
    field_id: int
    value: Union[int, str]
    created_at: datetime
    updated_at: datetime
    type: str
    name: str
    handle: Optional[str]


class OrderLine(BaseModel):
    id: int
    order_id: int
    full_sale_price: float
    total_price: float
    full_total_price: float
    discounts_amount: float
    quantity: int
    reserved_quantity: int
    weight: int
    dimensions: int
    variant_id: int
    product_id: int
    sku: str
    barcode: Union[str, int]
    title: str
    unit: str
    comment: Optional[str]
    created_at: datetime
    updated_at: datetime
    bundle_id: Optional[int]
    vat: int
    fiscal_product_type: int
    requires_marking: Optional[bool]
    marking_codes: Optional[str]
    accessory_lines: list


class OrderChange(BaseModel):
    id: int
    created_at: datetime
    action: str
    value_was: str
    value_is: str
    full_description: str
    user_name:str


class Order(BaseModel):
    field_values: list[FieldValue]
    order_lines: list[OrderLine]
    order_changes: list[OrderChange]
    discount: Optional[float]
    discounts: list
    # shipping_address
    # client
    total_price: float
    items_price: float
    id: int
    key: str
    number: int
    comment: Optional[str]
    archived: bool
    delivery_title: str
    delivery_description: str
    delivery_price: float
    full_delivery_price: float
    payment_description: str
    payment_title: str
    first_referer: HttpUrl
    first_current_location: str
    first_query: Optional[str]
    first_source_domain: str
    first_source: str
    referer: HttpUrl
    current_location: str
    query: Optional[str]
    source_domain: str
    source: str
    fulfillment_status: str
    custom_status: dict[str, str]
    delivered_at: datetime
    accepted_at: datetime
    created_at: datetime
    updated_at: datetime
    financial_status: str
    delivery_date: datetime
    delivery_from_hour: datetime
    delivery_from_minutes: datetime
    delivery_to_hour: datetime
    delivery_to_minutes: datetime
    paid_at: datetime
    delivery_variant_id: int
    payment_gateway_id: int
    margin: float
    client_transaction_id: Optional[int]
    currency_code: str
    cookies: dict[Optional[str, str]]
    account_id: int
    manager_comment: Optional[str]
    locale: str
    # delivery_info
    responsible_user_id: Optional[int]
    total_profit: float
    warehouse_id: int


class Orders(BaseModel):
    list: list[Order]
