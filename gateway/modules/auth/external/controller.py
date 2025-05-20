from fastapi import APIRouter, Depends, HTTPException, status

from .service import AuthService, get_service
from .models import LoginModel, TokenModel

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login", status_code=200, response_model=TokenModel)
async def login(request: LoginModel, service: AuthService = Depends(get_service)):
    response = await service.login(
        identifier=request.identifier,
        password=request.password,
    )

    token = response.get("token")

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas, tente novamente"
        )

    return TokenModel(token=token)