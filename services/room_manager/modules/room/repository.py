from fastapi import Depends
from dataclasses import dataclass
from bson import ObjectId

from room_manager.dependencies.database.client import get_database, Database

@dataclass
class RoomRepository:
    database: Database

    def update_room(self, room_id: str, data: dict) -> dict:
        update_data = {
            k: v for k, v in {
                "name": data.get("name"),
                "details": data.get("details"),
                "available": data.get("available"),
                "price": data.get("price"),
                "updated_at": data.get("updated_at")
            }.items() if v is not None
        }

        result = self.database["rooms"].update_one(
            {"_id": ObjectId(room_id)},
            {"$set": update_data}
        )

        if result.modified_count == 0:
            return None

        return self.get_internal_room(room_id)

    def get_internal_room(self, room_id: str) -> dict:
        room = self.database["rooms"].find_one({"_id": ObjectId(room_id)})
        if not room:
            return None
        return room

    def normalize_external_room(self, room: dict) -> dict:
        room.pop("_id")
        return room

    def get_room(self, external_id: str):
        room = self.database["rooms"].find_one({"external_id": external_id})
        return self.normalize_external_room(room)
    
    def get_room_by_external(self, external_id: str):
        return self.database["rooms"].find_one({"external_id": external_id})
    
    def filter_rooms(
        self,
        page: int,
        per_page: int,
        available: bool = None,
        min_price: float = None,
        max_price: float = None,
        checkin_date: str = None,
        checkout_date: str = None,
        search: str = None
    ):
        query = {}

        if search:
            search_regex = {"$regex": search, "$options": "i"}
            query["$or"] = [
                {"name": search_regex},
                {"details": search_regex},
            ]

        if min_price is not None:
            query["price"] = {"$gte": min_price}
        if max_price is not None:
            query.setdefault("price", {})["$lte"] = max_price

        rooms = list(self.database["rooms"].find(query))
        
        unavailable_room_ids = set()
        if checkin_date and checkout_date:
            conflicting_bookings = self.database["bookings"].find({
                "checkin_date": {"$lt": checkout_date},
                "checkout_date": {"$gt": checkin_date},
                "deleted_at": None,
                "payment_status": {"$ne": "REFUNDED"}
            })
            unavailable_room_ids = {booking["room_id"] for booking in conflicting_bookings}

        filtered_rooms = []
        for room in rooms:
            room_id = str(room["_id"])
            is_available = room.get("available", True) and room_id not in unavailable_room_ids

            if available is None or is_available == available:
                room["available"] = is_available
                filtered_rooms.append(self.normalize_external_room(room))

        total = len(filtered_rooms)
        paginated_rooms = filtered_rooms[(page - 1) * per_page: page * per_page]

        return {"rooms": paginated_rooms, "total": total}


def get_repository(database: Database = Depends(get_database)) -> RoomRepository:
    return RoomRepository(database=database)