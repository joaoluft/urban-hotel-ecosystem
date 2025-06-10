from fastapi import Depends
from dataclasses import dataclass
from bson import ObjectId
from datetime import datetime, timezone
from uuid import uuid4

from booking_manager.dependencies.database.client import get_database, Database

@dataclass
class BookingRepository:
    database: Database

    def get_booking(self, booking_id: str):
        return self.database["bookings"].find_one({"_id": ObjectId(booking_id)})
    
    def get_external_booking(self, external_id: str):
        return self.database["bookings"].find_one({"external_id": external_id})
    
    def create_booking(
        self,
        checkin_date: datetime,
        checkout_date: datetime,
        room_id: str,
        user_id: str,
        transaction_id: str,
        payment_status: str
    ) -> dict | None:
        booking = {
            "external_id": str(uuid4()),
            "checkin_date": checkin_date,
            "checkout_date": checkout_date,
            "room_id": room_id,
            "user_id": user_id,
            "transaction_id": transaction_id,
            "payment_status": payment_status,
            "created_at": datetime.now(timezone.utc),
            "updated_at": datetime.now(timezone.utc),
            "deleted_at": None
        }

        result = self.database["bookings"].insert_one(booking)

        if not result.acknowledged:
            return None

        booking["_id"] = result.inserted_id
        return booking

def get_repository(database: Database = Depends(get_database)) -> BookingRepository:
    return BookingRepository(database=database)