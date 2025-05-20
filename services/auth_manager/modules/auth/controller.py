from fastapi import APIRouter, Depends
from .service import AuthService, get_service
from .models import LoginModel, TokenModel

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login", status_code=200, response_model=TokenModel)
async def login(request: LoginModel, service: AuthService = Depends(get_service)):
    token = await service.login(
        identifier=request.identifier,
        password=request.password,
    )
    if not token:
        return TokenModel(token=None)
    
    return TokenModel(token=token)