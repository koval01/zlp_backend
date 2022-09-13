from typing import Any, List
from pydantic import BaseModel


class Product(BaseModel):
    id: int
    name: str
    price: int
    old_price: Any
    type: str
    number: int
    is_hidden: int
    commands: List[str]
    withdraw_commands: Any
    withdraw_commands_days: Any
    additional_fields: Any
    description: str = None
    category_id: Any
    image: str
    first_delete: int
    shop_id: int
    created_at: str
    updated_at: str
    sort_index: int


class ResponseItem(BaseModel):
    id: int
    name: str
    code: str
    sale: int
    limit: Any
    expires_at: str = None
    shop_id: int
    created_at: str
    updated_at: str
    products: List[Product]


class Model(BaseModel):
    success: bool
    response: List[ResponseItem]
