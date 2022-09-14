from typing import Any, List
from pydantic import BaseModel


class Server(BaseModel):
    id: int
    name: str
    ip: str
    port: str
    version: str
    is_port_hidden: int
    hide_ip: int
    is_hidden: int
    shop_id: int
    created_at: str
    updated_at: str


class Product(BaseModel):
    id: int
    product_id: int
    name: str
    price: int
    old_price: Any
    type: str
    number: int
    commands: List[str]
    additional_fields: Any
    description: Any
    payment_id: int
    amount: int
    image: str
    first_delete: int
    created_at: str
    updated_at: str


class Payment(BaseModel):
    id: int
    customer: str
    email: Any
    server_id: int
    payment_type: bool
    shop_id: int
    updated_at: str
    created_at: str
    enrolled: float
    cost: int
    server: Server
    products: List[Product]


class Response(BaseModel):
    url: str
    payment: Payment


class Model(BaseModel):
    success: bool
    response: Response | str
