from pydantic import BaseModel
from datetime import datetime

class BaseCodeModel(BaseModel):
    user_id: str
    code: str
    expiration: datetime
    used_at: datetime
    created_at: datetime