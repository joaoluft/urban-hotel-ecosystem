from fastapi import APIRouter

from .room.controller import router as room_router
from .booking.controller import router as booking_router
from .auth.external.controller import router as auth_external_router

api_router = APIRouter(prefix="/api")
external_router = APIRouter()

external_router.include_router(auth_external_router)

api_router.include_router(room_router)
api_router.include_router(booking_router)