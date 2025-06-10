from fastapi import Depends
from dataclasses import dataclass
from datetime import datetime

from gateway.dependencies.discovery.client import get_discovery, ServiceDiscovery

@dataclass
class BookingService:
    discovery: ServiceDiscovery

    async def create_booking(
            self, 
            user_external_id: str, 
            checkin_date: datetime,
            checkout_date: datetime,
            room_external_id: str,
            card_number: str,
            card_code: str,
            card_expiration_date: str
        ) -> bool:
        return await self.discovery.call_service(
            service_name="booking-manager",
            endpoint=f"/booking/",
            method="POST",
            json={
                "user_external_id": user_external_id,
                "checkin_date": checkin_date.isoformat(),
                "checkout_date": checkout_date.isoformat(),
                "room_external_id": room_external_id,
                "card_number": card_number,
                "card_code": card_code,
                "card_expiration_date": card_expiration_date
            }
        )
    
    async def delete_booking(
            self, 
            external_id: str,
        ) -> bool:
        return await self.discovery.call_service(
            service_name="booking-manager",
            endpoint=f"/booking/{external_id}",
            method="DELETE"
        )

def get_service(discovery: ServiceDiscovery = Depends(get_discovery)) -> BookingService:
    return BookingService(discovery=discovery)