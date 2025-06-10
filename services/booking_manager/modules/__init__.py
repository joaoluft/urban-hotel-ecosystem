from fastapi import APIRouter

from .booking.controller import router as booking_router

api_router = APIRouter()

# Include all routers here
api_router.include_router(booking_router)