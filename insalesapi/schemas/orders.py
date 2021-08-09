from datetime import datetime, date
from pydantic import BaseModel, HttpUrl
from typing import Optional, Union, Any

from .base import FieldValue
from .clients import Client


class OrderLine(BaseModel):
    id: int
    order_id: int
    full_sale_price: float
    total_price: float
    full_total_price: float
    discounts_amount: float
    quantity: int
    reserved_quantity: Optional[int]
    weight: Optional[float]
    dimensions: Optional[str]
    variant_id: int
    product_id: int
    sku: Optional[str]
    barcode: Optional[Union[int, str]]
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
    value_was: Any
    value_is: Any
    full_description: str
    user_name: Optional[str]


class Location(BaseModel):
    kladr_code: Optional[str]
    zip: Optional[int]
    region_zip: Optional[int]
    country: str
    state: str
    state_type: Optional[str]
    area: Optional[str]
    area_type: Optional[str]
    city: Optional[str]
    city_type: Optional[str]
    settlement: Optional[str]
    settlement_type: Optional[str]
    address: str
    street: Optional[str]
    street_type: Optional[str]
    house: Optional[str]
    flat: Optional[int]
    is_kladr: bool
    latitude: Optional[float]
    longitude: Optional[float]
    autodetected: Optional[bool]


class ShippingAddress(BaseModel):
    id: int
    fields_values: list[FieldValue]
    name: str
    surname: Optional[str]
    middlename: Optional[str]
    phone: str
    full_name: str
    full_locality_name: Optional[str]
    full_delivery_address: str
    address_for_gis: str
    location_valid: bool
    address: Optional[str]
    country: Optional[str]
    state: str
    city: Optional[str]
    zip: Optional[int]
    street: Optional[str]
    house: Optional[str]
    flat: Optional[str]
    location: Location


class DeliveryInterval(BaseModel):
    min_days: Optional[int]
    max_days: Optional[int]
    description: Optional[str]


class DeliveryInfo(BaseModel):
    delivery_variant_id: Optional[int]
    tariff_id: Optional[int]
    title: Optional[str]
    description: Optional[str]
    price: Optional[float]
    shipping_company: Optional[str]
    shipping_company_handle: Optional[str]
    delivery_interval: DeliveryInterval


class Order(BaseModel):
    fields_values: list[FieldValue]
    order_lines: list[OrderLine]
    order_changes: list[OrderChange]
    discount: Optional[Union[float, dict[str, Any]]]
    discounts: list
    shipping_address: ShippingAddress
    client: Client
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
    payment_description: Optional[str]
    payment_title: str
    first_referer: Optional[HttpUrl]
    first_current_location: Optional[str]
    first_query: Optional[str]
    first_source_domain: Optional[str]
    first_source: str
    referer: Optional[Union[HttpUrl, str]]
    current_location: Optional[str]
    query: Optional[str]
    source_domain: Optional[str]
    source: str
    fulfillment_status: str
    custom_status: dict[str, str]
    delivered_at: Optional[datetime]
    accepted_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime
    financial_status: str
    delivery_date: Optional[date]
    delivery_from_hour: Optional[int]
    delivery_from_minutes: Optional[int]
    delivery_to_hour: Optional[int]
    delivery_to_minutes: Optional[int]
    paid_at: Optional[datetime]
    delivery_variant_id: int
    payment_gateway_id: int
    margin: float
    client_transaction_id: Optional[int]
    currency_code: str
    cookies: Optional[dict[str, str]]
    account_id: int
    manager_comment: Optional[str]
    locale: str
    delivery_info: DeliveryInfo
    responsible_user_id: Optional[int]
    total_profit: float
    warehouse_id: Optional[int]


class Orders(BaseModel):
    list: list[Order]
