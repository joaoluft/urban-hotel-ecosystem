from pymongo import MongoClient
from pymongo.client_session import ClientSession
from threading import Lock
from typing import Optional
from dataclasses import dataclass
from .config import Settings

@dataclass
class Database:
    _instance: Optional["Database"] = None
    _lock: Lock = Lock()
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialize()
        return cls._instance
    
    def _initialize(self):
        self.settings = Settings()
        self.client = MongoClient(self.settings.database_url)
        self.db = self.client[self.settings.database_name]

    def __getitem__(self, collection_name: str):
        return self.db[collection_name]
    
    def start_session(self) -> ClientSession:
        return self.client.start_session()
    
    def close(self):
        self.client.close()

def get_database() -> Database:
    return Database()