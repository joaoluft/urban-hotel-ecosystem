from enum import Enum
from pydantic import BaseModel
from typing import Optional

class PaymentStatus(str, Enum):
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"

class PaymentResponseModel(BaseModel):
    status: PaymentStatus
    transaction_id: Optional[str] = None