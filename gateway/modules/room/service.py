from fastapi import Depends
from dataclasses import dataclass

from gateway.dependencies.discovery.client import get_discovery, ServiceDiscovery

@dataclass
class RoomService:
    discovery: ServiceDiscovery

    async def get_room(self, room_id: str):
        return await self.discovery.call_service(
            service_name="room-manager",
            endpoint=f"/room/{room_id}",
            method="GET"
        )

def get_service(discovery: ServiceDiscovery = Depends(get_discovery)) -> RoomService:
    return RoomService(discovery=discovery)