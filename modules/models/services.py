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


class ResponseItem(BaseModel):
    id: int
    name: str
    price: int
    old_price: Any
    type: str
    is_hidden: int
    number: int
    commands: List[str]
    withdraw_commands: Any
    withdraw_commands_days: Any
    additional_fields: Any
    description: str = None
    image: str
    first_delete: int
    shop_id: int
    created_at: str
    updated_at: str
    sort_index: int
    servers: List[Server]


class Model(BaseModel):
    success: bool
    response: List[ResponseItem]
