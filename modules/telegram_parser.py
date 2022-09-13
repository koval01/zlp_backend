import re

import aiohttp
from bs4 import BeautifulSoup


class TelegramParser:

    def __init__(self, choice: int, offset: int = None) -> None:
        choice_ = ['zalupa_history', 'zalupaonline']
        self.host = f"https://t.me/s/{choice_[choice]}?before={offset}"
        self.headers = {
            "Host":    "t.me",
            "Origin":  "https://t.me/",
            "Referer": "https://t.me/s/%s" % choice_[choice],
        }

    async def _request(self) -> str or None:
        async with aiohttp.ClientSession() as session:
            async with session.get(self.host, headers=self.headers) as resp:
                if resp.status < 400:
                    return await resp.text()

    @staticmethod
    def _parse(body: str) -> list:
        soup = BeautifulSoup(body.replace("\\", ""), "lxml")

        def finder(sp: BeautifulSoup, cl: str, tag: str = "div",
                   prettify: bool = False, text: bool = False, style: bool = False) \
                -> BeautifulSoup or None:

            if not sp:
                return None

            result = sp.find(tag, {"class": cl})
            if not result:
                return None

            return (result.text if text else result.prettify()) \
                if (prettify or text) \
                else (result["style"]) if style else result

        def selector(s: BeautifulSoup, cl: str) -> str or None:
            sl = finder(s, cl, "div")

            return re.sub(
                r"(<div.*?>)|(</div>)", "",
                str(sl).replace("<br/>", "<br>")
            ).strip() if sl else None

        def cover(s: BeautifulSoup) -> str:
            img = finder(s, "tgme_widget_message_photo_wrap", tag="a", style=True)
            thumb = finder(s, "tgme_widget_message_video_thumb", tag="i", style=True)

            if not img and not thumb:
                return ""
            style = img if img else thumb

            return re.search(r"background-image:url\('(.*?)'\)", style)[1]

        return [
            {
                "text": selector(m, "tgme_widget_message_text"),

                "name": finder(
                    finder(m, "tgme_widget_message_owner_name", tag="a"),
                    cl="", tag="span", text=True
                ),

                "author": finder(m, "tgme_widget_message_from_author", tag="span", text=True),
                "cover": cover(m),

                "datetime_utc": finder(
                    finder(m, "tgme_widget_message_date", tag="a"),
                    cl="time", tag="time"
                )["datetime"],

                "link": "https://t.me/s/" + re.search(
                    r"(https://t.me/)([A-z\d_\-]*?/\d*$)",
                    finder(
                        m, "tgme_widget_message_date", tag="a"
                    )["href"])[2]
            }
            for m in soup.find_all("div", {"class": "tgme_widget_message"})
            if selector(m, "tgme_widget_message_text")
        ]

    async def result(self) -> list:
        resp = await self._request()

        if not resp:
            return []
        return self._parse(resp)
