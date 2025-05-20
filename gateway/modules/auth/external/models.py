from pydantic import BaseModel

class LoginModel(BaseModel):
    identifier: str
    password: str

class TokenModel(BaseModel):
    token: str