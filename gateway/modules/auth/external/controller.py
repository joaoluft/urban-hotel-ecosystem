from fastapi import APIRouter, Depends, HTTPException, status

from .service import AuthService, get_service
from .models import (
    LoginResponseModel, 
    LoginRequestModel, 
    RegisterRequestModel,
    RegisterResponseModel,
    VerifyEmailRequestModel,
    VerifyEmailResponseModel,
    LoginStatusEnum
)

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login", status_code=200, response_model=LoginResponseModel)
async def login(request: LoginRequestModel, service: AuthService = Depends(get_service)):
    response = await service.login(
        identifier=request.identifier,
        password=request.password,
    )

    if response.get("status") == LoginStatusEnum.INVALID_CREDENTIALS.value:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas, tente novamente"
        )
    
    if response.get("status") == LoginStatusEnum.EMAIL_NOT_VERIFIED.value:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email não verificado, verifique seu e-mail para completar o registro"
        )

    return LoginResponseModel(
        id=response["id"],
        token=response["token"],
        username=response["username"],
        email=response["email"],
        status=response["status"]
    )

@router.post("/register", status_code=200, response_model=RegisterResponseModel)
async def register(request: RegisterRequestModel, service: AuthService = Depends(get_service)):
    result = await service.register(
        username=request.username,
        email=request.email,
        cpf=request.cpf,
        password=request.password,
        confirm_password=request.confirm_password
    )

    if not result.get("success"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Houve um problema ao registrar a conta"
        )
    
    return RegisterResponseModel(success=result["success"])

@router.post("/verify-email", status_code=200, response_model=VerifyEmailResponseModel)
async def verify_email(request: VerifyEmailRequestModel, service: AuthService = Depends(get_service)):
    result = await service.verify_email_code(code=request.code)

    if not result.get("success"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Houve um problema ao validar código de confirmação de e-mail"
        )
    
    return RegisterResponseModel(success=result["success"])