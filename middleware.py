from typing import Any, Callable, Coroutine
from fastapi import Response, Request


async def recaptcha_middleware(request: Request, call_next: Callable, some_attribute: Any) -> Response:
    request.state.attr = some_attribute
    return await call_next(request)
