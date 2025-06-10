from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class BookingModel(BaseModel):
    id: str
    external_id: str
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None

class BookingCreateModel(BaseModel):
    checkin_date: datetime
    checkout_date: datetime
    room_external_id: str
    user_external_id: str
    card_number: str
    card_code: str
    card_expiration_date: str

class BookingCreateResponseModel(BaseModel):
    success: bool

class BookingDeleteResponseModel(BookingCreateResponseModel):
    pass