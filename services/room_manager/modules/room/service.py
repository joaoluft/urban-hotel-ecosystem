from fastapi import Depends
from dataclasses import dataclass

from .repository import get_repository, RoomRepository

@dataclass
class RoomService:
    repository: RoomRepository

    def get_room(self, room_id: str):
        return self.repository.get_room(room_id=room_id)

def get_service(repository: RoomRepository = Depends(get_repository)) -> RoomService:
    return RoomService(repository=repository)