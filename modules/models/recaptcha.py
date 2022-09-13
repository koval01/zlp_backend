from typing import List
from pydantic import BaseModel, Field


class Model(BaseModel):
    success: bool = False
    challenge_ts: str
    hostname: str = None
    error_codes: List[str] = Field(None, alias='error-codes')
