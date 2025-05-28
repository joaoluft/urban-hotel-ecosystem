from pydantic import BaseModel
from typing import Optional

class RoomBaseModel(BaseModel):
    external_id: str
    name: str
    details: list[str]
    available: bool
    price: float

class RoomModel(RoomBaseModel):
    id: str
    owner_id: str
    created_at: str
    updated_at: str

class ExternalRoomModel(RoomBaseModel):
    pass

class RoomFiltersModel(BaseModel):
    page: int
    per_page: int
    available: Optional[bool] = None
    min_price: Optional[float] = None
    max_price: Optional[float] = None
    search: Optional[str] = None

class FilteredRoomsModel(BaseModel):
    items: list[ExternalRoomModel]
    total: int
    page: int
    per_page: int
    last_page: int