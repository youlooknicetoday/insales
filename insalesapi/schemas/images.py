from datetime import datetime
from pydantic import BaseModel
from typing import Optional


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