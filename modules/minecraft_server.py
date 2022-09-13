from mcstatus import JavaServer
from mcstatus.pinger import PingResponse
from logger import log


class StatusServer:

    def __init__(self, host: str = "zalupa.online:25565") -> None:
        self.host = host

    async def server(self) -> JavaServer:
        return await JavaServer.async_lookup(self.host)

    async def status(self) -> PingResponse or None:
        try:
            s = await self.server()
            return await s.async_status()
        except Exception as e:
            log.warning("Failed to get game server status. Exception: %s" % e)

    async def online(self) -> dict:
        status = await self.status()
        return {"online": status.players.online} \
            if status else {}
