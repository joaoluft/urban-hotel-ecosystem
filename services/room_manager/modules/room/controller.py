from fastapi import APIRouter, Depends

from .service import RoomService, get_service
from .models import RoomFiltersModel, FilteredRoomsModel, ExternalRoomModel

router = APIRouter(prefix="/room", tags=["room"])

@router.get("/{external_id}", status_code=200, response_model=ExternalRoomModel)
def get_room(external_id: str, service: RoomService = Depends(get_service)):
    return service.get_room(external_id)

@router.get("/", status_code=200, response_model=FilteredRoomsModel)
def filter_rooms(params: RoomFiltersModel = Depends(), service: RoomService = Depends(get_service)):
    return service.filter_rooms(params)