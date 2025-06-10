from pydantic import BaseModel
from datetime import datetime

class BookingCreateModel(BaseModel):
    checkin_date: datetime
    checkout_date: datetime
    room_external_id: str
    card_number: str
    card_code: str
    card_expiration_date: str

class BookingCreateResponseModel(BaseModel):
    success: bool