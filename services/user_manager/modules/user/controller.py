from fastapi import APIRouter, Depends

from .service import UserService, get_service
from .models import (
    CreateUserModel, 
    UpdateUserModel, 
    CreateUserResponse,
    UpdateUserResponse
)

router = APIRouter(prefix="/user", tags=["user"])

@router.get("/{user_id}", status_code=200)
def get_user(user_id: str, service: UserService = Depends(get_service)):
    return service.get_user(user_id)

@router.get("/external/{external_id}", status_code=200)
def get_external_user(external_id: str, service: UserService = Depends(get_service)):
    return service.get_external_user(external_id)

@router.get("/by-identifier/{identifier}", status_code=200)
def get_user_by_identifier(identifier: str, service: UserService = Depends(get_service)):
    return service.get_user_by_identifier(identifier)

@router.post("/", status_code=201, response_model=CreateUserResponse)
def create_user(request: CreateUserModel, service: UserService = Depends(get_service)):
    user_id = service.create_user(
        username=request.username,
        email=request.email,
        password=request.password,
        cpf=request.cpf
    )
    return CreateUserResponse(user_id=user_id)

@router.patch("/{user_id}", status_code=200, response_model=UpdateUserResponse)
def update_user(
    user_id: str,
    request: UpdateUserModel,
    service: UserService = Depends(get_service)
):
    updated = service.update_user(
        user_id=user_id,
        username=request.username,
        email=request.email,
        password=request.password,
        cpf=request.cpf,
        email_verified_at=request.email_verified_at
    )
    return UpdateUserResponse(success=updated)