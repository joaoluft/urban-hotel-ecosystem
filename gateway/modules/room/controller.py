from fastapi import APIRouter, Depends

from .service import RoomService, get_service

router = APIRouter(prefix="/room", tags=["room"])

@router.get("/{room_id}", status_code=200)
async def get_room(room_id: str, service: RoomService = Depends(get_service)):
    return await service.get_room(room_id)