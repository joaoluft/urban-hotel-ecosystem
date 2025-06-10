from fastapi import Depends
from dataclasses import dataclass
from typing import Optional
from datetime import datetime, timezone

from .repository import get_repository, UserRepository

@dataclass
class UserService:
    repository: UserRepository

    def get_user(self, user_id: str):
        return self.repository.get_user(user_id)
    
    def get_external_user(self, external_id: str):
        return self.repository.get_external_user(external_id)
    
    def get_user_by_identifier(self, identifier: str):
        return self.repository.get_user_by_identifier(identifier)
    
    def create_user(self, username: str, email: str, password: str, cpf: str) -> str:
        return self.repository.create_user(
            username=username,
            email=email,
            password=password,
            cpf=cpf
        )

    def update_user(
        self,
        user_id: str,
        username: Optional[str] = None,
        email: Optional[str] = None,
        password: Optional[str] = None,
        cpf: Optional[str] = None,
        email_verified_at: Optional[datetime] = None,
    ) -> bool:
        return self.repository.update_user(
            user_id=user_id,
            username=username,
            email=email,
            password=password,
            cpf=cpf,
            email_verified_at=email_verified_at
        )


def get_service(repository: UserRepository = Depends(get_repository)) -> UserService:
    return UserService(repository=repository)