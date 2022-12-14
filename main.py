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
    """Getting information about the game server and checking its availability"""

    return JSONResponse({
        "body": await StatusServer().online()
    })


@app.get("/channel_parse")
@limiter.limit("10/minute")
async def channel(request: Request, choice: int = 0, offset: int = None) -> JSONResponse:
    """Parsing posts from the Telegram channel"""

    return JSONResponse({
        "messages": await TelegramParser(
            choice, offset
        ).result()
    })


@app.post("/donate/services")
@limiter.limit("20/minute")
async def donate_services(request: Request, item: EasyDonate.Models.Services) \
        -> JSONResponse or HTTPException:
    """Getting a list of services"""

    if await ReCaptcha().check(item.token):
        return JSONResponse({
            "services": await EasyDonate.Services().get()
        })
    raise HTTPException(403, "ReCaptcha check error")


@app.post("/donate/coupon")
@limiter.limit("20/minute")
async def donate_coupon(request: Request, item: EasyDonate.Models.Coupon) \
        -> JSONResponse or HTTPException:
    """Checking the coupon and returning information about it"""

    if await ReCaptcha().check(item.token):
        return JSONResponse({
            "coupon": await EasyDonate.Coupon().get(item.code)
        })
    raise HTTPException(403, "ReCaptcha check error")


@app.post("/donate/payment_get")
@limiter.limit("20/minute")
async def donate_payment(request: Request, item: EasyDonate.Models.Payment) \
        -> JSONResponse or HTTPException:
    """Receipt of check details"""

    if await ReCaptcha().check(item.token):
        return JSONResponse({
            "payment": await EasyDonate.Payment().get(
                item.payment_id, item.tokens_send
            )
        })
    raise HTTPException(403, "ReCaptcha check error")


@app.post("/donate/payment/create")
@limiter.limit("20/minute")
async def donate_payment(request: Request, item: EasyDonate.Models.Bill) \
        -> JSONResponse or HTTPException:
    """Create a check for payment"""

    if await ReCaptcha().check(item.token):
        return JSONResponse(await EasyDonate.Bill().send(
            success_url=item.success_url,
            products=item.products,
            customer=item.customer,
            email=item.email,
            coupon=item.coupon
        ))
    raise HTTPException(403, "ReCaptcha check error")

