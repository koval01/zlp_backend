from mcstatus import JavaServer
from mcstatus.pinger import PingResponse
from logger import log


class StatusServer:

    def __init__(self, host: str = "zalupa.online:25565") -> None:
        self.server = JavaServer.lookup(host)

    def status(self) -> PingResponse or None:
        try:
            return self.server.status()
        except Exception as e:
            log.warning("Failed to get game server status. Exception: %s" % e)

    def online(self) -> dict:
        status = self.status()
        return {"online": status.players.online} \
            if status else {}
