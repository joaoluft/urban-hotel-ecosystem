from pydantic import BaseModel

class LoginRequestModel(BaseModel):
    identifier: str
    password: str

class LoginResponseModel(BaseModel):
    id: str
    token: str
    username: str
    email: str