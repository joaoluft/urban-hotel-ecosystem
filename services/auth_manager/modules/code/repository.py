from fastapi import Depends
from dataclasses import dataclass
from datetime import datetime, timezone, timedelta

from auth_manager.dependencies.database.client import get_database, Database
from .utils import generate_code_string

@dataclass
class CodeRepository:
    database: Database

    def get(self, code: str) -> dict:
        return self.database["codes"].find_one({ "code": code })

    def create(self, user_id: str, expiration_minutes: int = 300):
        now = datetime.now(timezone.utc)
        expiration = now + timedelta(minutes=expiration_minutes)

        code = generate_code_string(8)

        code_data = {
            "user_id": user_id,
            "code": code,
            "expiration": expiration,
            "used_at": None,
            "created_at": now
        }

        self.database["codes"].insert_one(code_data)

        return code
    
    def update(self, code: str, used_at: datetime) -> None:
        now = datetime.now(timezone.utc)
        self.database["codes"].update_one(
            { "code": code },
            { 
                "$set": { 
                    "used_at": used_at,
                    "updated_at": now
                } 
            }
        )

def get_repository(database: Database = Depends(get_database)) -> CodeRepository:
    return CodeRepository(database=database)