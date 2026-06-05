import asyncio

from fastapi import FastAPI, Request

from aiogram import Bot, Dispatcher
from aiogram.types import Update

from app.core.config import settings
from app.database.database import db

from app.middlewares.antiflood import AntiFloodMiddleware

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

# BOT + DP
bot = Bot(token=settings.BOT_TOKEN)
dp = Dispatcher()

app = FastAPI()


# -------------------------
# STARTUP
# -------------------------
async def startup():
    await db.connect()
    await db.create_tables()

    # middleware
    dp.message.middleware(AntiFloodMiddleware())

    # routers
    dp.include_router(start.router)
    dp.include_router(admin.router)
    dp.include_router(whitelist.router)
    dp.include_router(moderation.router)
    dp.include_router(group_settings.router)
    dp.include_router(welcome.router)
    dp.include_router(member_events.router)
    dp.include_router(group_security.router)

    # webhook set
    await bot.set_webhook(
        url=settings.WEBHOOK_URL,
        drop_pending_updates=True
    )


@app.on_event("startup")
async def on_startup():
    await startup()


# -------------------------
# WEBHOOK
# -------------------------
@app.post("/webhook")
async def telegram_webhook(request: Request):

    data = await request.json()

    update = Update.model_validate(data)

    await dp.feed_update(bot, update)

    return {"status": "ok"}