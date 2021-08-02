from datetime import datetime
from pydantic import BaseModel
from typing import Optional, Union

from .images import Image


class ProductOptionName(BaseModel):
    id: int
    position: int
    navigational: bool
    title: str


class ProductOptionNames(BaseModel):
    list: list[ProductOptionName]


class ProductProperty(BaseModel):
    id: int
    position: int
    is_hidden: bool
    is_navigational: bool
    backoffice: bool
    permalink: str
    title: str


class ProductProperties(BaseModel):
    list: list[ProductProperty]


class ProductFieldValue(BaseModel):
    id: int
    product_field_id: int
    value: Optional[str]


class ProductFieldValues(BaseModel):
    list: list[ProductFieldValue]


class ProductOptionValue(BaseModel):
    id: int
    option_name_id: int
    position: int
    title: str


class ProductVariant(BaseModel):
    available: bool
    id: int
    title: str
    product_id: int
    sku: Optional[str]
    quantity: Optional[int]
    quantity_at_warehouse0: Optional[float]
    barcode: Optional[Union[str, int]]
    dimensions: Optional[str]
    weight: Optional[float]
    price: float
    price_in_site_currency: float
    prices: list[Optional[float]]
    prices_in_site_currency: list[Optional[float]]
    base_price: float
    base_price_in_site_currency: float
    cost_price: Optional[float]
    cost_price_in_site_currency: Optional[float]
    old_price: Optional[float]
    old_price_in_site_currency: Optional[float]
    option_values: list[ProductOptionValue]
    created_at: datetime
    updated_at: datetime
    variant_field_values: list
    image_id: Optional[int]
    image_ids: list[Optional[int]]


class ProductBundleComponent(BaseModel):
    id: int
    variant_id: int
    free: bool
    quantity: int
    discount_amount: Optional[float]
    product_id: int
    discount_type: Optional[str]


class Product(BaseModel):
    id: int
    category_id: int
    created_at: datetime
    updated_at: datetime
    is_hidden: bool
    available: bool
    archived: bool
    canonical_url_collection_id: Optional[int]
    custom_template: Optional[bool]
    unit: str
    sort_weight: Optional[float]
    ignore_discounts: Optional[bool]
    vat: int
    dimensions: Optional[str]
    fiscal_product_type: int
    title: str
    short_description: Optional[str]
    permalink: str
    html_title: Optional[str]
    meta_keywords: Optional[str]
    meta_description: Optional[str]
    currency_code: str
    collections_ids: list[int]
    images: list[Image]
    option_names: list[ProductOptionName]
    properties: list[ProductProperty]
    product_field_values: list[ProductFieldValue]
    variants: list[ProductVariant]
    product_bundle_components: list
    description: Optional[str]


class Products(BaseModel):
    __root__: list[Product]
