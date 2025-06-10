from fastapi import APIRouter, Depends

from .service import BookingService, get_service
from .models import (
    BookingCreateModel, 
    BookingCreateResponseModel, 
    BookingDeleteResponseModel
)

router = APIRouter(prefix="/booking", tags=["booking"])

@router.get("/list/{user_external_id}", status_code=200)
async def list_bookings(user_external_id: str, service: BookingService = Depends(get_service)):
    return await service.list_bookings(user_external_id=user_external_id)

@router.get("/{booking_id}", status_code=200)
def get_booking(booking_id: str, service: BookingService = Depends(get_service)):
    return service.get_booking(booking_id)

@router.post("/", status_code=200, response_model=BookingCreateResponseModel)
async def create_booking(request: BookingCreateModel, service: BookingService = Depends(get_service)):
    booking = await service.create_booking(
        checkin_date=request.checkin_date,
        checkout_date=request.checkout_date,
        room_external_id=request.room_external_id,
        user_external_id=request.user_external_id,
        card_number=request.card_number,
        card_code=request.card_code,
        card_expiration_date=request.card_expiration_date
    )
    
    return BookingCreateResponseModel(success=booking)

@router.delete("/{external_id}", status_code=200, response_model=BookingDeleteResponseModel)
async def delete_booking(external_id: str, service: BookingService = Depends(get_service)):
    delete = await service.delete_booking(external_id=external_id)
    return BookingDeleteResponseModel(success=delete)