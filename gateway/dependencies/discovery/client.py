from typing import Optional, Dict, Any
from dataclasses import dataclass, field
from .config import Settings
import consul as consul_lib
import httpx
import asyncio
from concurrent.futures import ThreadPoolExecutor


@dataclass
class ServiceDiscovery:
    settings: Settings = field(default_factory=Settings)
    consul: consul_lib.Consul = field(init=False)
    executor: ThreadPoolExecutor = field(default_factory=ThreadPoolExecutor)

    def __post_init__(self):
        self.consul = consul_lib.Consul(
            host=self.settings.discovery_host,
            port=self.settings.discovery_port
        )

    def _get_service_sync(self, service_name: str) -> Optional[str]:
        try:
            _, services = self.consul.catalog.service(service_name)
            if not services:
                return None
            service = services[0]
            address = service["ServiceAddress"] or service["Address"]
            port = service["ServicePort"]
            return f"http://{address}:{port}"
        except Exception as e:
            print(f"[Discovery] service not found: '{service_name}': {e}")
            return None

    async def get_service(self, service_name: str) -> Optional[str]:
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(self.executor, self._get_service_sync, service_name)

    async def call_service(
        self,
        service_name: str,
        endpoint: str,
        method: str = "GET",
        headers: Optional[Dict[str, str]] = None,
        params: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
    ) -> Any:
        base_url = await self.get_service(service_name)
        if not base_url:
            raise ValueError(f"[Discovery] Service not found: '{service_name}'")

        url = f"{base_url}{endpoint}"
        try:
            async with httpx.AsyncClient(timeout=5) as client:
                response = await client.request(
                    method=method,
                    url=url,
                    headers=headers,
                    params=params,
                    json=json
                )
                response.raise_for_status()

                try:
                    return response.json()
                except ValueError:
                    return response.text
                

        except httpx.HTTPStatusError as e:
            raise Exception(f"[Discovery] HTTP error calling '{service_name}': {e.response.status_code} - {e.response.text}") from e
        except httpx.RequestError as e:
            raise Exception(f"[Discovery] Request error calling '{service_name}': {str(e)}") from e

def get_discovery() -> ServiceDiscovery:
    return ServiceDiscovery()
