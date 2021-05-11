from pydantic import BaseModel
from typing import Optional, Union
from datetime import datetime


class OrderLine(BaseModel):
    id: Optional[int]
    order_id: Optional[int]
    sale_price: int
    full_sale_price: int
    total_price: int
    full_total_price: int
    discounts_amount: int
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
    updated_at: Optional[datetime]
    created_at: Optional[datetime]
    bundle_id: Optional[int]
    vat: int


class Order(BaseModel):
    order_lines: list[OrderLine]
