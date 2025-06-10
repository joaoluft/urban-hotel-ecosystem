from fastapi import FastAPI
from typing import AsyncGenerator
from consul import Consul
from auth_manager.core.config import Settings

async def lifespan(app: FastAPI) -> AsyncGenerator:
    settings: Settings = Settings()
    consul = Consul(
        host=settings.discovery_host, 
        port=settings.discovery_port
    )

    service_identifier = "auth-manager"
    service_port = 8001
    check_url = f"http://auth-manager:{service_port}/health"

    consul.agent.service.register(
        service_identifier,
        port=service_port,
        address=service_identifier,
        check={
            'http': check_url,
            'interval': '10s'
        }
    )

    yield

    consul.agent.service.deregister(service_identifier)