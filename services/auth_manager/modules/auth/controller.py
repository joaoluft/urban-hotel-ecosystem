from fastapi import APIRouter, Depends, status, HTTPException
from .service import AuthService, get_service
from .models import LoginRequestModel, LoginResponseModel

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login", status_code=200, response_model=LoginResponseModel)
async def login(request: LoginRequestModel, service: AuthService = Depends(get_service)):
    user = await service.login(
        identifier=request.identifier,
        password=request.password,
    )
    if not user:
        return HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )
    
    return LoginResponseModel(
        id=user.id,
        token=user.token,
        username=user.username,
        email=user.email,
    )