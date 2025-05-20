from pydantic import BaseModel
from typing import Optional

class LoginModel(BaseModel):
    identifier: str
    password: str

class TokenModel(BaseModel):
    token: Optional[str] = None