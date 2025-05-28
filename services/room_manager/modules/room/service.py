from fastapi import Depends
from dataclasses import dataclass

from .repository import get_repository, RoomRepository
from .models import RoomFiltersModel, FilteredRoomsModel

@dataclass
class RoomService:
    repository: RoomRepository

    def get_room(self, room_id: str):
        return self.repository.get_room(room_id=room_id)
    
    def filter_rooms(self, filters: RoomFiltersModel) -> FilteredRoomsModel:
        query = self.repository.filter_rooms(
            page=filters.page,
            per_page=filters.per_page,
            available=filters.available,
            min_price=filters.min_price,
            max_price=filters.max_price,
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