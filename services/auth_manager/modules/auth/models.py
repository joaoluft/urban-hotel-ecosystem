from enum import Enum
from pydantic import BaseModel, EmailStr
from typing import Optional

class LoginStatusEnum(str, Enum):
    INVALID_CREDENTIALS = "INVALID_CREDENTIALS"
    EMAIL_NOT_VERIFIED = "EMAIL_NOT_VERIFIED"
    SUCCESS = "SUCCESS"

class LoginRequestModel(BaseModel):
    identifier: str
    password: str

class LoginResponseModel(BaseModel):
    id: Optional[str] = None
    token: Optional[str] = None
    username: Optional[str] = None
    email: Optional[str] = None
    status: Optional[LoginStatusEnum]

class RegisterRequestModel(BaseModel):
    username: str
    email: EmailStr
    cpf: str
    password: str
    confirm_password: str

class RegisterResponseModel(BaseModel):
    success: bool

class VerifyEmailResponseModel(BaseModel):
    success: bool

class VerifyEmailRequestModel(BaseModel):
    code: str