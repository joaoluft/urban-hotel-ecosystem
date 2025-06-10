from enum import Enum
from pydantic import BaseModel
from typing import Optional

class PaymentStatus(str, Enum):
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    REFUNDED = "REFUNDED"

class PaymentResponseModel(BaseModel):
    status: PaymentStatus
    transaction_id: Optional[str] = None

class RefundResponseModel(BaseModel):
    status: PaymentStatus
    refund_id: Optional[str] = None