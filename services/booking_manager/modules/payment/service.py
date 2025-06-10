from fastapi import Depends
from dataclasses import dataclass
from datetime import date

from booking_manager.dependencies.payment.client import get_payment_gateway, PaymentGateway
from .models import PaymentStatus, PaymentResponseModel, RefundResponseModel

@dataclass
class PaymentService:
    gateway: PaymentGateway

    async def process_payment(self, card_number: str, expiration_date: str, code: str, amount: float) -> PaymentResponseModel:
        payment = await self.gateway.process_payment(
            {
                "card_number": card_number, 
                "expiration_date": expiration_date, 
                "code": code, 
                "amount": amount
            }
        )

        if not payment:
            return PaymentResponseModel(status=PaymentStatus.FAILED)
        
        if payment.get("status") == PaymentStatus.SUCCESS.value:
            return PaymentResponseModel(
                status=PaymentStatus.SUCCESS, 
                transaction_id=payment.get("transaction_id")
            )
        
    async def refund_payment(self, transaction_id: id) -> PaymentStatus:
        refund = await self.gateway.process_refund({"transaction_id": transaction_id})

        if not refund:
            return RefundResponseModel(status=PaymentStatus.FAILED)
        
        if refund.get("status") == PaymentStatus.SUCCESS.value:
            return RefundResponseModel(
                status=PaymentStatus.REFUNDED, 
                refund_id=refund.get("refund_id")
            )

def get_service(gateway: PaymentGateway = Depends(get_payment_gateway)) -> PaymentService:
    return PaymentService(gateway=gateway)