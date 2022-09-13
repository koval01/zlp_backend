from typing import Any, List
from pydantic import BaseModel


class SentCommand(BaseModel):
    command: str
    response: str


class Product(BaseModel):
    id: int
    name: str
    price: int
    old_price: Any
    type: str
    number: int
    commands: List[str]
    withdraw_commands: Any
    withdraw_commands_days: Any
    additional_fields: Any
    description: Any
    image: str
    first_delete: int
    shop_id: int
    created_at: str
    updated_at: str
    sort_index: int


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


class Response(BaseModel):
    id: int
    customer: str
    email: Any
    shop_id: int
    server_id: int
    status: int
    enrolled: int
    payment_system: str
    payment_type: str
    sent_commands: List[SentCommand]
    error: Any
    created_at: str
    updated_at: str
    products: List[Product]
    server: Server


class Model(BaseModel):
    success: bool
    response: Response
