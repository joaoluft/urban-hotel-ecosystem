from fastapi import APIRouter, Depends, HTTPException

from .service import RoomService, get_service
from .models import (
    RoomFiltersModel, 
    FilteredRoomsModel, 
    ExternalRoomModel, 
    RoomModel, 
    RoomUpdateModel,
    RoomUpdateResponseModel
)

router = APIRouter(prefix="/room", tags=["room"])

@router.get("/{external_id}", status_code=200, response_model=ExternalRoomModel)
def get_room(external_id: str, service: RoomService = Depends(get_service)):
    return service.get_room(external_id)

@router.get("/by-external-id/{external_id}", status_code=200, response_model=RoomModel)
def get_room(external_id: str, service: RoomService = Depends(get_service)):
    return service.get_room_by_external(external_id)

@router.get("/", status_code=200, response_model=FilteredRoomsModel)
def filter_rooms(params: RoomFiltersModel = Depends(), service: RoomService = Depends(get_service)):
    return service.filter_rooms(params)

@router.get("/internal/{room_id}", status_code=200, response_model=RoomModel)
def get_internal_room(room_id: str, service: RoomService = Depends(get_service)):
    room = service.get_internal_room(room_id)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    
    return room

@router.patch("/{room_id}", status_code=200, response_model=RoomUpdateResponseModel)
def get_internal_room(room_id: str, data: RoomUpdateModel, service: RoomService = Depends(get_service)):
    updated = service.update_room(room_id=room_id, data=data)
    return RoomUpdateResponseModel(success=updated)
