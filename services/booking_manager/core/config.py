from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    discovery_host: str = "consul"
    discovery_port: int = 8500
    frontend_url: str = "http://localhost:8080"

def get_settings() -> Settings:
    return Settings()