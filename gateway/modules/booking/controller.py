from fastapi import APIRouter, Depends, Request

from .service import BookingService, get_service
from .models import BookingCreateModel, BookingCreateResponseModel

router = APIRouter(prefix="/booking", tags=["booking"])

@router.post("/", status_code=200, response_model=BookingCreateResponseModel)
async def create_booking(
    payload: BookingCreateModel,
    request: Request,
    service: BookingService = Depends(get_service),
):
    user = request.state.user
    result = await service.create_booking(
        user_external_id=user["user_id"],
        checkin_date=payload.checkin_date,
        checkout_date=payload.checkout_date,
        room_external_id=payload.room_external_id,
        card_number=payload.card_number,
        card_code=payload.card_code,
        card_expiration_date=payload.card_expiration_date
    )
    return BookingCreateResponseModel(success=result["success"])

@router.delete("/{external_id}", status_code=200)
async def delete_booking(
    external_id: str,
    service: BookingService = Depends(get_service),
):
    result = await service.delete_booking(
        external_id=external_id
    )
    return {"success": result["success"]}

@router.get("/list", status_code=200)
async def list_bookings(request: Request, service: BookingService = Depends(get_service)):
    user = request.state.user
    return await service.list_bookings(user_external_id=user["user_id"])