from datetime import datetime
from pydantic import BaseModel
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
