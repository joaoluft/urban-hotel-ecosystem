from dataclasses import dataclass, field
from typing import Dict, Any
import httpx

from .config import Settings

@dataclass
class PaymentGateway:
    settings: Settings = field(default_factory=Settings)
    client: httpx.AsyncClient = field(init=False)

    def __post_init__(self):
        self.client = httpx.AsyncClient(base_url=self.settings.payment_gateway_url)

    async def process_payment(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        response = await self.client.post("/payment", json=payload)
        response.raise_for_status()
        return response.json()

    async def process_refund(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        response = await self.client.post("/refund", json=payload)
        response.raise_for_status()
        return response.json()

    async def __aexit__(self, *args):
        await self.client.aclose()

def get_payment_gateway() -> PaymentGateway:
    return PaymentGateway()