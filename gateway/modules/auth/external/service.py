from fastapi import Depends
from dataclasses import dataclass

from gateway.dependencies.discovery.client import get_discovery, ServiceDiscovery

@dataclass
class AuthService:
    discovery: ServiceDiscovery

    async def login(self, identifier: str, password: str) -> str:
        return await self.discovery.call_service(
            service_name="auth-manager",
            endpoint=f"/auth/login",
            method="POST",
            json={
                "identifier": identifier,
                "password": password,
            },
        )

def get_service(discovery: ServiceDiscovery = Depends(get_discovery)) -> AuthService:
    return AuthService(discovery=discovery)