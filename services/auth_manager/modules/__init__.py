from fastapi import APIRouter

from .auth.controller import router as auth_router

api_router = APIRouter()

# Include all routers here
api_router.include_router(auth_router)