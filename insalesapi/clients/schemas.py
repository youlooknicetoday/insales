from datetime import datetime
from pydantic import BaseModel, IPvAnyAddress
from typing import Optional, Union

from ..src.schemas import FieldValue


class Client(BaseModel):
    id: int
    email: Optional[str]
    name: str
    phone: str
    created_at: datetime
    updated_at: str
    registered: bool
    subscribe: bool
    client_group_id: Optional[int]
    surname: Optional[str]
    middlename: Optional[str]
    bonus_points: int
    type: str
    correspondent_account: Optional[str]
    settlement_account: Optional[str]
    consent_to_personal_data: Optional[str]
    progressive_discount: Optional[str]
    group_discount: Optional[str]
    ip_addr: Union[IPvAnyAddress, str]
    fields_values = list[FieldValue]
