import json
import os
from typing import Dict

import aiohttp
from dotenv import load_dotenv
from pydantic import BaseModel

from modules.models import bill as bill_model
from modules.models import coupon as coupon_model
from modules.models import payment as payment_model
from modules.models import services as services_model
from modules.models.coupon import ResponseItem as ResponseItemCoupon
from modules.models.payment import ResponseItem as ResponseItemPayment
from modules.models.services import ResponseItem as ResponseItemServices
from modules.special import StringEditor

load_dotenv()


class EasyDonate:
    host = "https://easydonate.ru/api/v3"
    api_key = os.getenv("SECRET_KEY_DONATE")

    class Models:

        class Services(BaseModel):
            token: str

        class Coupon(BaseModel):
            code: str
            token: str

        class Payment(BaseModel):
            payment_id: int
            token: str
            tokens_send: bool

        class Bill(BaseModel):
            customer: str
            coupon: str = None
            email: str = None
            products: Dict[int, int]
            success_url: str
            token: str

    @staticmethod
    async def request(headers: dict, path: str, params: dict = None) -> dict:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                    f"{EasyDonate.host}/{path}", headers=headers, params=params
            ) as resp:
                if resp.status < 400:
                    body = await resp.json()
                    return body
        return {}

    class Services:

        @staticmethod
        def _products(response: list[ResponseItemServices]) -> list:
            return [{
                "id": product.id,
                "name": product.name,
                "description": product.description,
                "image": product.image,
                "price": product.price,
                "old_price": product.old_price,
                "type": product.type,
                "number": product.number
            } for product in response if not product.is_hidden]

        async def get(self) -> list:
            response = await EasyDonate.request({
                "Shop-Key": EasyDonate.api_key
            }, "shop/products")
            data = services_model.Model(**response)
            if data.success:
                return self._products(data.response)
            return []

    class Coupon:

        @staticmethod
        def _select_coupon(data: list[ResponseItemCoupon], name: str) -> list[ResponseItemCoupon] or None:
            result = [c for c in data if c.code == name] if len(data) else None
            return result[0] if result else {}

        @staticmethod
        def _builder(data: ResponseItemCoupon) -> dict:
            products = [
                {
                    "id": p.id, "name": p.name
                } for p in data.products
            ] if data else []

            return {
                "code": data.code,
                "discount": data.sale,
                "products": products
            } if data else {}

        async def get(self, coupon: str) -> dict:
            response = await EasyDonate.request({
                "Shop-Key": EasyDonate.api_key
            }, "shop/coupons", params={
                "where_active": "true"
            })

            data = coupon_model.Model(**response)
            selected = self._select_coupon(data.response, coupon) \
                if data.success and len(coupon) else {}

            return self._builder(selected)

    class Payment:

        @staticmethod
        def _get_tokens_paid(data: ResponseItemPayment, coins_mode: bool) -> int:
            if coins_mode:
                pattern = data.products[0].commands[0]
                exc_com = data.sent_commands[0].command

                ground_pattern = pattern.split("\x20")
                ground_exc_com = exc_com.split("\x20")

                for i, el in enumerate(ground_pattern):
                    if el == "{amount}":
                        return int(ground_exc_com[i])

            return 0

        @staticmethod
        def _status(status: int) -> bool:
            return True if status == 2 else False

        def _builder(self, data: ResponseItemPayment, coins_mode: bool) -> dict:
            return {
                "id": data.id,
                "customer": data.customer,
                "email": StringEditor.censor_email(data.email),
                "created_at": data.created_at,
                "payment_system": data.payment_system,
                "status": self._status(data.status),
                "enrolled": self._get_tokens_paid(data, coins_mode)
            }

        async def get(self, bill_id: int, coins_mode: bool = True) -> dict:
            response = await EasyDonate.request({
                "Shop-Key": EasyDonate.api_key
            }, f"shop/payment/{bill_id}")

            data = payment_model.Model(**response)

            return self._builder(data.response, coins_mode=coins_mode) \
                if data.success else {}

    class Bill:

        @staticmethod
        async def _request(params: dict) -> dict:
            response = await EasyDonate.request({
                "Shop-Key": EasyDonate.api_key
            }, f"shop/payment/create", params=params)

            return response

        async def send(self, success_url: str, products: dict, customer: str, email: str = "", coupon: str = "") \
                -> dict:
            response = await self._request({
                "customer": customer,
                "server_id": os.getenv("SERVER_ID"),
                "products": json.dumps(products),
                "email": email,
                "coupon": coupon,
                "success_url": success_url
            })
            data = bill_model.Model(**response)

            return {
                "url": data.response.url,
                "bill_id": data.response.payment.id
            } if data.success else {}
