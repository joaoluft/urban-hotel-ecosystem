from fastapi import APIRouter

from .user.controller import router as user_router

api_router = APIRouter()

# Include all routers here
api_router.include_router(user_router)