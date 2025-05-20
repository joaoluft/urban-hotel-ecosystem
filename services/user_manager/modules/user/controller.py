from fastapi import APIRouter, Depends

from .service import UserService, get_service

router = APIRouter(prefix="/user", tags=["user"])

@router.get("/{user_id}", status_code=200)
def get_user(user_id: str, service: UserService = Depends(get_service)):
    return service.get_room(user_id)

@router.get("/by-identifier/{identifier}", status_code=200)
def get_user_by_identifier(identifier: str, service: UserService = Depends(get_service)):
    return service.get_user_by_identifier(identifier)