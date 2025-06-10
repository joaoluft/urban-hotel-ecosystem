from fastapi import Depends
from dataclasses import dataclass

from .repository import get_repository, RoomRepository
from .models import (
    RoomFiltersModel, 
    FilteredRoomsModel, 
    ExternalRoomModel, 
    RoomModel, 
    RoomUpdateModel
)

@dataclass
class RoomService:
    repository: RoomRepository

    def update_room(self, room_id: str, data: RoomUpdateModel) -> bool:
        updated = self.repository.update_room(
            room_id=room_id,
            data=data.model_dump(exclude_unset=True, exclude_defaults=True)
        )
        if not updated:
            return False
        
        return True

    def get_internal_room(self, room_id: str) -> RoomModel | None:
        room = self.repository.get_internal_room(room_id)
        if not room:
            return None
        
        return RoomModel(
            id=str(room["_id"]),
            external_id=room["external_id"],
            name=room["name"],
            details=room["details"],
            available=room["available"],
            price=room["price"],
            owner_id=room["owner_id"],
            created_at=room["created_at"],
            updated_at=room["updated_at"]
        )

    def get_room(self, external_id: str) -> ExternalRoomModel:
        room: ExternalRoomModel = self.repository.get_room(external_id)
        return ExternalRoomModel(
            external_id=room["external_id"],
            name=room["name"],
            details=room["details"],
            available=room["available"],
            price=room["price"]
        )
    
    def get_room_by_external(self, external_id: str) -> RoomModel:
        room: ExternalRoomModel = self.repository.get_room_by_external(external_id)
        return RoomModel(
            id=str(room["_id"]),
            external_id=room["external_id"],
            name=room["name"],
            details=room["details"],
            available=room["available"],
            price=room["price"],
            owner_id=room["owner_id"],
            created_at=room["created_at"],
            updated_at=room["updated_at"]
        )
    
    def filter_rooms(self, filters: RoomFiltersModel) -> FilteredRoomsModel:
        query = self.repository.filter_rooms(
            page=filters.page,
            per_page=filters.per_page,
            available=filters.available,
            min_price=filters.min_price,
            max_price=filters.max_price,
            checkin_date=filters.checkin_date,
            checkout_date=filters.checkout_date,
            search=filters.search
        )
        return FilteredRoomsModel(
            items=query["rooms"],
            total=query["total"],
            page=filters.page,
            per_page=filters.per_page,
            last_page=(query["total"] + filters.per_page - 1) // filters.per_page
        )

def get_service(repository: RoomRepository = Depends(get_repository)) -> RoomService:
    return RoomService(repository=repository)