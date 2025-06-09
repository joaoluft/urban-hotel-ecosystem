from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class UserModel(BaseModel):
    id: str
    external_id: str
    username: str
    email: str
    password: str
    email_verified_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime
    
class CreateUserModel(BaseModel):
    username: str
    email: str
    password: str
    cpf: str

class UpdateUserModel(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    cpf: Optional[str] = None
    email_verified_at: Optional[datetime] = None

class CreateUserResponse(BaseModel):
    user_id: str

class UpdateUserResponse(BaseModel):
    success: bool