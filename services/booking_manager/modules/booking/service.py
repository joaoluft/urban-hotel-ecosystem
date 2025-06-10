from fastapi import Depends
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from .repository import get_repository, BookingRepository
from booking_manager.modules.payment.service import PaymentService, get_service as get_payment_service
from booking_manager.modules.payment.models import PaymentStatus
from booking_manager.dependencies.discovery.client import get_discovery, ServiceDiscovery
from booking_manager.dependencies.email.client import Email, get_email
from .utils import format_date_ptbr, format_brl
from booking_manager.core.config import Settings, get_settings

@dataclass
class BookingService:
    repository: BookingRepository
    payment_service: PaymentService
    discovery: ServiceDiscovery
    email: Email
    settings: Settings

    async def list_bookings(self, user_external_id: str):
        user = await self.discovery.call_service(
            service_name="user-manager",
            endpoint=f"/user/external/{user_external_id}",
            method="GET"
        )

        if not user:
            return []
        
        return self.repository.list_bookings(user_id=user["_id"])

    def get_booking(self, booking_id: str):
        return self.repository.get_booking(booking_id)
    
    async def _get_available_room(self, room_external_id: str):
        try:
            room = await self.discovery.call_service(
                service_name="room-manager",
                endpoint=f"/room/by-external-id/{room_external_id}",
                method="GET"
            )
            if not room or not room.get("available", False):
                return None
            return room
        except Exception as e:
            print(f"[Booking] Room fetch failed: {e}")
            return None

    def _calculate_total_amount(self, price_per_day: float, checkin: datetime, checkout: datetime) -> float:
        nights = (checkout - checkin).days + 1
        return price_per_day * nights

    async def _process_payment(self, card_number: str, expiration: str, code: str, amount: float) -> Optional[PaymentStatus]:
        try:
            return await self.payment_service.process_payment(
                card_number=card_number,
                expiration_date=expiration,
                code=code,
                amount=amount
            )
        except Exception as e:
            print(f"[Booking] Payment failed: {e}")
            return None
        
    async def _send_email_confirmation(
            self, 
            to: str, 
            total_amount: float, 
            room_name: str,
            checkin_date: datetime,
            checkout_date: datetime,
            username: str
        ) -> None:
        
        formatted_checkin = format_date_ptbr(checkin_date)
        formatted_checkout = format_date_ptbr(checkout_date)
        formatted_amount = format_brl(total_amount)

        await self.email.send_email(
            to=[to],
            subject="Confirmação de reserva | Urban Hotel",
            template_name="booking_confirmation.html",
            context={
                "total_amount": formatted_amount,
                "room_name": room_name,
                "checkin_date": formatted_checkin,
                "checkout_date": formatted_checkout,
                "username": username,
                "my_bookings_link": f"{self.settings.frontend_url}/my-bookings"
            }
        )

    async def _send_email_cancelation(
            self, 
            to: str, 
            total_amount: float, 
            room_name: str,
            checkin_date: datetime,
            checkout_date: datetime,
            username: str
        ) -> None:
        
        formatted_checkin = format_date_ptbr(checkin_date)
        formatted_checkout = format_date_ptbr(checkout_date)
        formatted_amount = format_brl(total_amount)

        await self.email.send_email(
            to=[to],
            subject="Cancelamento de reserva | Urban Hotel",
            template_name="booking_cancelation.html",
            context={
                "total_amount": formatted_amount,
                "room_name": room_name,
                "checkin_date": formatted_checkin,
                "checkout_date": formatted_checkout,
                "username": username,
                "rooms_page_link": f"{self.settings.frontend_url}/rooms",
                "cancellation_date": format_date_ptbr(datetime.now())
            }
        )

    async def _mark_room_unavailable(self, room_id: str) -> bool:
        try:
            result = await self.discovery.call_service(
                service_name="room-manager",
                endpoint=f"/room/{room_id}",
                method="PATCH",
                json={"available": False}
            )
            return bool(result)
        except Exception as e:
            print(f"[Booking] Room update failed: {e}")
            return False

    def _store_booking(
        self,
        checkin: datetime,
        checkout: datetime,
        room_id: str,
        user_id: str,
        payment: PaymentStatus,
        amount: float
    ) -> bool:
        try:
            return bool(self.repository.create_booking(
                checkin_date=checkin,
                checkout_date=checkout,
                room_id=room_id,
                user_id=user_id,
                transaction_id=payment.transaction_id,
                payment_status=payment.status.value,
                amount=amount
            ))
        except Exception as e:
            print(f"[Booking] DB insert failed: {e}")
            return False


    async def create_booking(
        self, 
        checkin_date: datetime, 
        checkout_date: datetime, 
        room_external_id: str, 
        user_external_id: str,
        card_number: str,
        card_code: str,
        card_expiration_date: str,
    ) -> bool:
        user = await self.discovery.call_service(
            service_name="user-manager",
            endpoint=f"/user/external/{user_external_id}",
            method="GET"
        )

        if not user:
            return False
        
        room = await self._get_available_room(room_external_id)
        if not room:
            return False

        amount = self._calculate_total_amount(room["price"], checkin_date, checkout_date)

        payment = await self._process_payment(
            card_number, card_expiration_date, card_code, amount
        )

        if payment.status != PaymentStatus.SUCCESS:
            return False

        if not await self._mark_room_unavailable(room["id"]):
            return False

        store = self._store_booking(
            checkin_date, checkout_date, room["id"], user["_id"], payment, amount
        )

        if not store:
            return False

        await self._send_email_confirmation(
            to=user["email"],
            total_amount=amount,
            room_name=room["name"],
            checkin_date=checkin_date,
            checkout_date=checkout_date,
            username=user["username"]
        )

        return store
    
    async def delete_booking(self, external_id: str) -> bool:
        booking = self.repository.get_external_booking(external_id)
        if not booking or booking.get("deleted_at"):
            return False
        
        room = await self.discovery.call_service(
            service_name="room-manager",
            endpoint=f"/room/{booking['room_id']}",
            method="PATCH",
            json={ "available": True }
        )

        if not room:
            return False
        
        user = await self.discovery.call_service(
            service_name="user-manager",
            endpoint=f"/user/{booking["user_id"]}",
            method="GET"
        )

        if not user:
            return False
        
        room = await self.discovery.call_service(
            service_name="room-manager",
            endpoint=f"/room/internal/{booking["room_id"]}",
            method="GET"
        )
        
        if not room:
            return False
        
        refund = await self.payment_service.refund_payment(booking["transaction_id"])
        
        if refund.status != PaymentStatus.REFUNDED:
            return False
        
        deleted = self.repository.delete_booking(
            external_id=external_id,
            refund_id=refund.refund_id
        )

        if not deleted:
            return False
        
        await self._send_email_cancelation(
            to=user["email"],
            total_amount=booking["amount"],
            room_name=room["name"],
            checkin_date=booking["checkin_date"],
            checkout_date=booking["checkout_date"],
            username=user["username"]
        )

        return deleted

def get_service(
        repository: BookingRepository = Depends(get_repository),
        payment_service: PaymentService = Depends(get_payment_service),
        discovery: ServiceDiscovery = Depends(get_discovery),
        email: Email = Depends(get_email),
        settings: Settings = Depends(get_settings)
    ) -> BookingService:
    return BookingService(
        repository=repository, 
        payment_service=payment_service,
        discovery=discovery,
        email=email,
        settings=settings
    )