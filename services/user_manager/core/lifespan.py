from fastapi import FastAPI
from typing import AsyncGenerator
from consul import Consul
from user_manager.core.config import Settings

async def lifespan(app: FastAPI) -> AsyncGenerator:
    settings: Settings = Settings()
    consul = Consul(
        host=settings.discovery_host, 
        port=settings.discovery_port
    )

    service_identifier = "user-manager"
    service_port = 8003
    check_url = f"http://user-manager:{service_port}/health"

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