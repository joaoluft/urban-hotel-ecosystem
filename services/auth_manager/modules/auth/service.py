from datetime import datetime, timedelta, timezone
from fastapi import Depends
from dataclasses import dataclass
from argon2.exceptions import VerifyMismatchError
from jwt import encode

from auth_manager.dependencies.discovery.client import get_discovery, ServiceDiscovery
from auth_manager.core.config import Settings, get_settings
from auth_manager.core.hasher import get_password_hasher, PasswordHasher
from .models import LoginResponseModel

@dataclass
class AuthService:
    discovery: ServiceDiscovery
    config: Settings
    hasher: PasswordHasher

    async def login(self, identifier: str, password: str) -> LoginResponseModel | None:
        user = await self.discovery.call_service(
            service_name="user-manager",
            endpoint=f"/user/by-identifier/{identifier}",
            method="GET",
        )

        if not user:
            return None

        try:
            self.hasher.verify(user["password"], password)
        except VerifyMismatchError:
            return None

        now = datetime.now(timezone.utc)
        payload = {
            "user_id": user["external_id"],
            "iss": self.config.jwt_issuer,
            "exp": now + timedelta(seconds=self.config.jwt_expiration),
        }

        token = encode(
            payload=payload,
            key=self.config.jwt_secret,
            algorithm=self.config.jwt_algorithm,
        )

        return LoginResponseModel(
            id=user["external_id"],
            token=token,
            username=user["username"],
            email=user["email"],
        )

def get_service(
    discovery: ServiceDiscovery = Depends(get_discovery),
    config: Settings = Depends(get_settings),
    hasher: PasswordHasher = Depends(get_password_hasher),
) -> AuthService:
    return AuthService(discovery=discovery, config=config, hasher=hasher)