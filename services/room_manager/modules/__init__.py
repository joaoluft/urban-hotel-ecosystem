from fastapi import APIRouter

from .room.controller import router as room_router

api_router = APIRouter()

# Include all routers here
api_router.include_router(room_router)