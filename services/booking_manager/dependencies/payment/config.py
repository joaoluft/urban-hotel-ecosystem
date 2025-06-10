from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    payment_gateway_url: str = "http://payment-gateway:8085"