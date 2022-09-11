from fastapi import FastAPI, Request
from fastapi.exceptions import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

from modules.easydonate import EasyDonate
from modules.minecraft_server import StatusServer
from modules.recaptcha import ReCaptcha
from modules.telegram_parser import TelegramParser

limiter = Limiter(key_func=get_remote_address)
app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/server")
@limiter.limit("30/minute")
async def server(request: Request) -> JSONResponse:
    return JSONResponse({"body": StatusServer().online()})


@app.get("/channel_parse")
@limiter.limit("10/minute")
async def channel(request: Request, choice: int = 0, offset: int = None) -> JSONResponse:
    return JSONResponse({"messages": await TelegramParser(choice, offset).result()})


@app.post("/donate/services")
@limiter.limit("20/minute")
async def donate_services(request: Request, item: EasyDonate.Models.Services) -> JSONResponse or HTTPException:
    if await ReCaptcha().check(item.token):
        return JSONResponse({"services": await EasyDonate.Services().get()})
    raise HTTPException(403, "ReCaptcha check error")


@app.post("/donate/coupon")
@limiter.limit("20/minute")
async def donate_services(request: Request, item: EasyDonate.Models.Coupon) -> JSONResponse or HTTPException:
    if await ReCaptcha().check(item.token):
        return JSONResponse({"coupon": await EasyDonate().coupon_check(item.code)})
    raise HTTPException(403, "ReCaptcha check error")


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
