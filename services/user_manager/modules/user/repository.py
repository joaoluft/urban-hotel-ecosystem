from fastapi import Depends
from dataclasses import dataclass

from user_manager.dependencies.database.client import get_database, Database

@dataclass
class UserRepository:
    database: Database

    def get_user(self, user_id: str):
        return self.database["users"].find_one({"external_id": user_id})
    
    def get_user_by_identifier(self, identifier: str):
        user = self.database["users"].find_one({
            "$or": [
                {"email": identifier},
                {"username": identifier}
            ]
        })
        
        if user:
            user["_id"] = str(user["_id"]) 

        return user

def get_repository(database: Database = Depends(get_database)) -> UserRepository:
    return UserRepository(database=database)