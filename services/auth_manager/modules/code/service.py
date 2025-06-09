from fastapi import Depends
from dataclasses import dataclass
from datetime import datetime

from auth_manager.dependencies.email.client import Email, get_email
from auth_manager.dependencies.discovery.client import get_discovery, ServiceDiscovery
from .repository import CodeRepository, get_repository
from auth_manager.core.config import get_settings, Settings

@dataclass
class CodeService:
    email: Email
    repository: CodeRepository
    discovery: ServiceDiscovery
    settings: Settings

    async def send_email_confirmation_code(self, to: str, user_id: str) -> bool:
        code = self.repository.create(
            user_id=user_id, 
            expiration_minutes=300
        )

        if code:
            await self.email.send_email(
                to=[to],
                subject="Confirmação de e-mail | Urban Hotel",
                template_name="email_confirmation.html",
                context={
                    "confirmation_link": f"{self.settings.frontend_url}/email-confirmation/{code}",
                    "username": "João Luft"
                },
            )
            return True
        
        return False
    
    async def verify_email_confirmation_code(self, code: str) -> bool:
        existing_code = self.repository.get(code=code)
        print(existing_code)
        if not existing_code:
            return False
        
        if existing_code["used_at"] is not None:
            return False
        
        
        now = datetime.now().replace(tzinfo=None)
        if existing_code["created_at"] >= now >= existing_code["expiration"]:
            return False

        update_user = await self.discovery.call_service(
            service_name="user-manager",
            endpoint=f"/user/{existing_code["user_id"]}",
            method="PATCH",
            json={ "email_verified_at": now.isoformat() }
        )

        if not update_user["success"]:
            return False
        
        self.repository.update(code=code, used_at=now)
        
        return True

def get_service(
    email: Email = Depends(get_email),
    repository: CodeRepository = Depends(get_repository),
    discovery: ServiceDiscovery = Depends(get_discovery),
    settings: Settings = Depends(get_settings)
) -> CodeService:
    return CodeService(
        email=email, 
        repository=repository, 
        discovery=discovery,
        settings=settings
    )