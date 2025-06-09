from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    jwt_secret: str = "Unknown"
    jwt_expiration: int = 3600
    jwt_issuer: str = "urban_hotel"
    jwt_algorithm: str = "HS256"
    frontend_url: str = "http://localhost:8080"

def get_settings() -> Settings:
    return Settings()