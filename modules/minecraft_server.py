from mcstatus import JavaServer


class StatusServer:

    def __init__(self, host: str = "zalupa.online:25565") -> None:
        self.server = JavaServer.lookup(host)
        self.status = self.server.status()

    def online(self) -> dict:
        return {"online": self.status.players.online}
