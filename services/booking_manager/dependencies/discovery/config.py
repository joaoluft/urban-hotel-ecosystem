from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    discovery_host: str = "consul"
    discovery_port: int = 8500