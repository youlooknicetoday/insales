from typing import Optional, Any
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
    description: Optional[str]
    seo_description: Optional[str]


class Collections(BaseModel):
    list: list[Collection]
