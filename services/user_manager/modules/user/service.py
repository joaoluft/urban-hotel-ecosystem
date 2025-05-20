from fastapi import Depends
from dataclasses import dataclass

from .repository import get_repository, UserRepository

@dataclass
class UserService:
    repository: UserRepository

    def get_user(self, user_id: str):
        return self.repository.get_user(user_id)
    
    def get_user_by_identifier(self, identifier: str):
        return self.repository.get_user_by_identifier(identifier)


def get_service(repository: UserRepository = Depends(get_repository)) -> UserService:
    return UserService(repository=repository)