from fastapi import APIRouter, Depends

from .service import RoomService, get_service
from .models import RoomFiltersModel, FilteredRoomsModel

router = APIRouter(prefix="/room", tags=["room"])

@router.get("/{external_id}", status_code=200)
async def get_room(external_id: str, service: RoomService = Depends(get_service)):
    return await service.get_room(external_id)

@router.get("/", status_code=200, response_model=FilteredRoomsModel)
async def filter_rooms(params: RoomFiltersModel = Depends(), service: RoomService = Depends(get_service)):
    return await service.filter_rooms(params)