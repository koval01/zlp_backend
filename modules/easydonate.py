import os

import aiohttp
from pydantic import BaseModel


class EasyDonate:

    host = "https://easydonate.ru/api/v3"
    api_key = os.getenv("SECRET_KEY_DONATE")

    class Models:

        class Services(BaseModel):
            token: str

        class Coupon(BaseModel):
            code: str
            token: str

    @staticmethod
    async def request(headers: dict, path: str, params: dict = None) -> dict:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{EasyDonate.host}/{path}", headers=headers, params=params) as resp:
                if resp.status < 400:
                    body = await resp.json()
                    return body
        return {}

    class Services:

        @staticmethod
        def _products(response: list) -> list:
            return [{
                "id": product["id"],
                "name": product["name"],
                "description": product["description"],
                "image": product["image"],
                "price": product["price"],
                "old_price": product["old_price"],
                "type": product["type"],
                "number": product["number"]
            } for product in response if not product["is_hidden"]]

        async def get(self) -> list:
            response = await EasyDonate.request({
                "Shop-Key": EasyDonate.api_key
            }, "shop/products")
            if response["success"]:
                return self._products(response["response"])
            return []

    # @staticmethod
    # def _check_key(array: list, key: str, value: str) -> bool:
    #     return True in [True for k in array if k[key] == value]
    #
    # def _coupon_response_build(self, response: list, coupon: str) -> dict:
    #     select_coupon = self._check_key(response, "code", coupon)
    #     if select_coupon:
    #         pass
    #     return {}
    #
    # async def coupon_check(self, coupon: str) -> dict:
    #     response = await self._request({
    #         "Shop-Key": self.api_key
    #     }, "shop/coupons", params={
    #         "where_active": "true"
    #     })
    #     return {}
