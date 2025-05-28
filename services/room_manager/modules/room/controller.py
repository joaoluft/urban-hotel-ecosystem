from fastapi import APIRouter, Depends

from .service import RoomService, get_service
from .models import RoomFiltersModel, FilteredRoomsModel

router = APIRouter(prefix="/room", tags=["room"])

@router.get("/{room_id}", status_code=200)
def get_room(room_id: str, service: RoomService = Depends(get_service)):
    return service.get_room(room_id)

@router.get("/", status_code=200, response_model=FilteredRoomsModel)
def filter_rooms(params: RoomFiltersModel = Depends(), service: RoomService = Depends(get_service)):
    return service.filter_rooms(params)