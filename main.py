import asyncio

from fastapi import FastAPI
from fastapi import Request
from fastapi import HTTPException

from aiogram import Bot
from aiogram import Dispatcher
from aiogram.types import Update

from app.core.config import settings

from app.database.database import db

from app.middlewares.antiflood import (
    AntiFloodMiddleware
)

from app.handlers import (
    start,
    admin,
    whitelist,
    moderation,
    settings as group_settings,
    welcome,
    group_security,
    member_events
)

bot = Bot(
    token=settings.BOT_TOKEN
)

dp = Dispatcher()

app = FastAPI()


async def startup():

    await db.connect()

    await db.create_tables()

    dp.message.middleware(
        AntiFloodMiddleware()
    )

    dp.include_router(
        start.router
    )

    dp.include_router(
        admin.router
    )

    dp.include_router(
        whitelist.router
    )

    dp.include_router(
        moderation.router
    )

    dp.include_router(
        group_settings.router
    )

    dp.include_router(
        welcome.router
    )

    dp.include_router(
        member_events.router
    )

    dp.include_router(
        group_security.router
    )

    await bot.set_webhook(
        url=settings.WEBHOOK_URL,
        secret_token=settings.WEBHOOK_SECRET
    )


@app.on_event("startup")
async def on_startup():
    await startup()


@app.post("/webhook")
async def telegram_webhook(
    request: Request
):

    secret = request.headers.get(
        "X-Telegram-Bot-Api-Secret-Token"
    )

    if secret != settings.WEBHOOK_SECRET:
        raise HTTPException(
            status_code=403
        )

    data = await request.json()

    update = Update.model_validate(
        data
    )

    await dp.feed_update(
        bot,
        update
    )

    return {
        "status": "ok"
    }