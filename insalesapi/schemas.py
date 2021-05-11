from typing import Union, Optional, Any
from pydantic import BaseModel
from datetime import datetime


class FieldValue(BaseModel):
    id: int
    value: str


class Collection(BaseModel):
    id: int
    parent_id: int
    created_at: datetime
    updated_at: datetime
    is_hidden: bool
    position: int
    sort_type: int
    custom_template: Any
    recursive: Optional[bool]
    is_smart: Optional[bool]
    title: str
    html_title: Optional[str]
    meta_description: Optional[str]
    meta_keywords: Optional[str]
    permalink: str
    url: str
    field_values: list[FieldValue]
    description: str
    seo_description: str


class Collections(BaseModel):
    list: list[Collection]


class Image(BaseModel):
    id: int
    product_id: int
    position: int
    created_at: datetime
    image_processing: bool
    external_id: Optional[str]
    title: Optional[str]
    url: str
    original_url: str
    medium_url: str
    small_url: str
    thumb_url: str
    compact_url: str
    large_url: str
    filename: str


class Images(BaseModel):
    list: list[Image]


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
    value: str


class ProductFieldValues(BaseModel):
    list: list[ProductFieldValue]


class ProductOptionValue(BaseModel):
    id: int
    option_name_id: int
    position: int
    title: str


class ProductVariant(BaseModel):
    variant_field_values: list
    id: int
    title: str
    product_id: int
    sku: str
    barcode: Optional[Union[str, int]]
    dimensions: Optional[str]
    available: bool
    image_ids: list[int]
    created_at: datetime
    updated_at: datetime
    quantity: Optional[int]
    cost_price: Optional[float]
    cost_price_in_site_currency: Optional[float]
    price_in_site_currency: float
    base_price: float
    old_price: Optional[float]
    price2: Optional[float]
    price: float
    base_price_in_site_currency: float
    old_price_in_site_currency: Optional[float]
    price2_in_site_currency: Optional[float]
    prices: list[float]
    prices_in_site_currency: list[float]
    option_values: list[ProductOptionValue]


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
    canonical_url_collection_id: int
    custom_template: Optional[bool]
    unit: str
    sort_weight: Optional[float]
    ignore_discounts: Optional[bool]
    vat: int
    dimensions: str
    fiscal_product_type: int
    title: str
    short_description: str
    permalink: str
    html_title: Optional[str]
    meta_keywords: Optional[str]
    meta_description: Optional[str]
    currency_code: str
    collections_ids: list[int]
    images: Images
    option_names: ProductOptionNames
    properties: ProductProperties
    product_field_values: ProductFieldValues
    variants: list[ProductVariant]
    product_bundle_components: list
    description: str
