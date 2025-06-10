from uuid import uuid4
from datetime import datetime, timezone
from fastapi import Depends
from dataclasses import dataclass
from typing import Optional
from bson import ObjectId

from user_manager.dependencies.database.client import get_database, Database

@dataclass
class UserRepository:
    database: Database

    def get_user(self, user_id: str):
        return self.database["users"].find_one({"_id": ObjectId(user_id)})
    
    def get_external_user(self, external_id: str):
        user = self.database["users"].find_one({"external_id": external_id})
        return {**user, "_id": str(user["_id"])} if user else None
    
    def get_user_by_identifier(self, identifier: str):
        user = self.database["users"].find_one({
            "$or": [
                {"email": identifier},
                {"username": identifier},
                {"cpf": identifier}
            ]
        })
        
        if user:
            user["_id"] = str(user["_id"]) 

        return user
    
    def create_user(self, username: str, email: str, password: str, cpf: str) -> str:
        now = datetime.now(timezone.utc)

        user = self.database["users"].insert_one({
            "external_id": str(uuid4()),
            "username": username,
            "cpf": cpf,
            "email": email,
            "password": password,
            "created_at": now,
            "updated_at": now
        })
        
        return str(user.inserted_id)

    def update_user(
        self,
        user_id: str,
        username: Optional[str] = None,
        email: Optional[str] = None,
        password: Optional[str] = None,
        cpf: Optional[str] = None,
        email_verified_at: Optional[datetime] = None,
    ) -> bool:
        now = datetime.now(timezone.utc)

        update_fields = {
            "updated_at": now
        }

        if username is not None:
            update_fields["username"] = username
        if email is not None:
            update_fields["email"] = email
        if password is not None:
            update_fields["password"] = password
        if cpf is not None:
            update_fields["cpf"] = cpf
        if email_verified_at is not None:
            update_fields["email_verified_at"] = email_verified_at

        result = self.database["users"].update_one(
            {"_id": ObjectId(user_id)},
            {"$set": update_fields}
        )

        if result.matched_count == 0:
            raise ValueError(f"User with external_id '{user_id}' not found")
        
        return result.modified_count > 0

def get_repository(database: Database = Depends(get_database)) -> UserRepository:
    return UserRepository(database=database)