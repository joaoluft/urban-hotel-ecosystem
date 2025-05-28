from fastapi import APIRouter, Depends, HTTPException, status

from .service import AuthService, get_service
from .models import LoginResponseModel, LoginRequestModel

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login", status_code=200, response_model=LoginResponseModel)
async def login(request: LoginRequestModel, service: AuthService = Depends(get_service)):
    response = await service.login(
        identifier=request.identifier,
        password=request.password,
    )

    if not response:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas, tente novamente"
        )

    return LoginResponseModel(
        id=response["id"],
        token=response["token"],
        username=response["username"],
        email=response["email"]
    )
