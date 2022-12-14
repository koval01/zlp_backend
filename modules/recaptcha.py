import os
from dotenv import load_dotenv


import aiohttp

from modules.models import recaptcha

load_dotenv()


class ReCaptcha:

    def __init__(self) -> None:
        self.host = "https://www.google.com/recaptcha/api/siteverify"
        self.key = os.getenv("RE_SECRET")

    async def _request(self, data: dict) -> dict:
        async with aiohttp.ClientSession() as session:
            async with session.post(self.host, data=data) as resp:
                if resp.status < 400:
                    return await resp.json()
        return {}

    async def check(self, token: str) -> bool:
        json = await self._request({
            "secret": self.key,
            "response": token
        })
        data = recaptcha.Model(**json)
        return data.success if data else False
