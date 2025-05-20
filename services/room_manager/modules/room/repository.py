from fastapi import Depends
from dataclasses import dataclass

from room_manager.dependencies.database.client import get_database, Database

@dataclass
class RoomRepository:
    database: Database

    def get_room(self, room_id: str):
        return self.database["rooms"].find_one({"external_id": room_id})

def get_repository(database: Database = Depends(get_database)) -> RoomRepository:
    return RoomRepository(database=database)