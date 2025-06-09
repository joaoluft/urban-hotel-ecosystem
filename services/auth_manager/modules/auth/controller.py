from fastapi import APIRouter, Depends, status, HTTPException
from .service import AuthService, get_service
from .models import (
    LoginRequestModel, 
    LoginResponseModel, 
    RegisterRequestModel, 
    RegisterResponseModel,
    VerifyEmailRequestModel,
    VerifyEmailResponseModel,
    LoginStatusEnum
)

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login", status_code=200, response_model=LoginResponseModel)
async def login(request: LoginRequestModel, service: AuthService = Depends(get_service)):
    login = await service.login(
        identifier=request.identifier,
        password=request.password,
    )

    if login.status == LoginStatusEnum.INVALID_CREDENTIALS:
        return LoginResponseModel(status=LoginStatusEnum.INVALID_CREDENTIALS)
    
    if login.status == LoginStatusEnum.EMAIL_NOT_VERIFIED:
        return LoginResponseModel(status=LoginStatusEnum.EMAIL_NOT_VERIFIED)
    
    return LoginResponseModel(
        id=login.id,
        token=login.token,
        username=login.username,
        email=login.email,
        status=login.status
    )

@router.post("/register", status_code=200, response_model=RegisterResponseModel)
async def register(request: RegisterRequestModel, service: AuthService = Depends(get_service)):
    registered = await service.register(
        username=request.username,
        email=request.email,
        cpf=request.cpf,
        password=request.password,
        confirm_password=request.confirm_password
    )

    if not registered:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Houve um problema ao registrar a conta"
        )
    
    return RegisterResponseModel(success=registered)

@router.post("/verify-email", status_code=200, response_model=VerifyEmailResponseModel)
async def verify_email(request: VerifyEmailRequestModel, service: AuthService = Depends(get_service)):
    confirmed = await service.verify_email_code(code=request.code)

    if not confirmed:
        return RegisterResponseModel(success=False)
    
    return RegisterResponseModel(success=confirmed)