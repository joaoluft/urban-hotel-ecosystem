from datetime import datetime, timedelta, timezone
from fastapi import Depends
from dataclasses import dataclass
from argon2.exceptions import VerifyMismatchError
from jwt import encode

from auth_manager.dependencies.discovery.client import get_discovery, ServiceDiscovery
from auth_manager.dependencies.email.client import Email, get_email
from auth_manager.dependencies.cpf_validator.client import CPFValidator, get_cpf_validator
from auth_manager.core.config import Settings, get_settings
from auth_manager.core.hasher import get_password_hasher, PasswordHasher
from .models import LoginResponseModel, LoginStatusEnum

from auth_manager.modules.code.service import CodeService, get_service as get_code_service

@dataclass
class AuthService:
    discovery: ServiceDiscovery
    config: Settings
    hasher: PasswordHasher
    email: Email
    code_service: CodeService
    cpf_validator: CPFValidator

    async def login(self, identifier: str, password: str) -> LoginResponseModel | None:
        user = await self.discovery.call_service(
            service_name="user-manager",
            endpoint=f"/user/by-identifier/{identifier}",
            method="GET",
        )

        if not user:
            return LoginResponseModel(status=LoginStatusEnum.INVALID_CREDENTIALS)
        
        if not user.get("email_verified_at"):
            return LoginResponseModel(status=LoginStatusEnum.EMAIL_NOT_VERIFIED)

        try:
            self.hasher.verify(user["password"], password)
        except VerifyMismatchError:
            return LoginResponseModel(status=LoginStatusEnum.INVALID_CREDENTIALS)

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
            status=LoginStatusEnum.SUCCESS
        )
    
    async def validate_existing_user(self, email: str, username: str, cpf: str) -> bool:
        existing_email = await self.discovery.call_service(
            service_name="user-manager",
            endpoint=f"/user/by-identifier/{email}",
            method="GET"
        )

        if existing_email:
            return True
        
        existing_username = await self.discovery.call_service(
            service_name="user-manager",
            endpoint=f"/user/by-identifier/{username}",
            method="GET"
        )

        if existing_username:
            return True
        
        existing_cpf = await self.discovery.call_service(
            service_name="user-manager",
            endpoint=f"/user/by-identifier/{cpf}",
            method="GET"
        )

        if existing_cpf:
            return True
    
    async def register(self, username: str, email: str, cpf: str, password: str, confirm_password: str) -> bool:
        if password != confirm_password:
            return False
        
        if not self.cpf_validator.is_valid(cpf=cpf):
            return False
        
        existing_user = await self.validate_existing_user(
            email=email, 
            username=username, 
            cpf=cpf
        )

        if existing_user:
            return False

        hashed_password = self.hasher.hash(password)
        
        created_user = await self.discovery.call_service(
            service_name="user-manager",
            endpoint="/user/",
            method="POST",
            json={
                "username": username,
                "email": email,
                "password": hashed_password,
                "cpf": cpf
            }
        )

        if not created_user:
            return False

        email_delivered = await self.code_service.send_email_confirmation_code(
            to=email,
            user_id=created_user["user_id"]
        )

        if not email_delivered:
            return False
        
        return True
    
    def verify_email_code(self, code: str) -> bool:
        return self.code_service.verify_email_confirmation_code(code=code)

def get_service(
    discovery: ServiceDiscovery = Depends(get_discovery),
    config: Settings = Depends(get_settings),
    hasher: PasswordHasher = Depends(get_password_hasher),
    email: Email = Depends(get_email),
    code_service: CodeService = Depends(get_code_service),
    cpf_validator: CPFValidator = Depends(get_cpf_validator)
) -> AuthService:
    return AuthService(
        discovery=discovery, 
        config=config, 
        hasher=hasher, 
        email=email, 
        code_service=code_service,
        cpf_validator=cpf_validator
    )