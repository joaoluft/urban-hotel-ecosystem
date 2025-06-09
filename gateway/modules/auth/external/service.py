from fastapi import Depends
from dataclasses import dataclass

from gateway.dependencies.discovery.client import get_discovery, ServiceDiscovery

@dataclass
class AuthService:
    discovery: ServiceDiscovery

    async def login(self, identifier: str, password: str) -> str | bool:
        try:
            return await self.discovery.call_service(
                service_name="auth-manager",
                endpoint=f"/auth/login",
                method="POST",
                json={
                    "identifier": identifier,
                    "password": password,
                },
            )
        except Exception as e:
            print(f"[AuthService] Error during login: {e}")
            return False
    
    async def register(self, username: str, email: str, cpf: str, password: str, confirm_password: str) -> bool:
        try:
            return await self.discovery.call_service(
            service_name="auth-manager",
            endpoint=f"/auth/register",
            method="POST",
            json={
                "username": username,
                "email": email,
                "cpf": cpf,
                "password": password,
                "confirm_password": confirm_password
            },
        )
        except Exception as e:
            print(f"[AuthService] Error during registration: {e}")
            return False
    
    async def verify_email_code(self, code: str) -> bool:
        try:
            return await self.discovery.call_service(
                service_name="auth-manager",
                endpoint=f"/auth/verify-email",
                method="POST",
                json={ "code": code },
            )
        except Exception as e:
            print(f"[AuthService] Error during email verification: {e}")
            return False

def get_service(discovery: ServiceDiscovery = Depends(get_discovery)) -> AuthService:
    return AuthService(discovery=discovery)