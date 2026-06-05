import time

from aiogram import BaseMiddleware
from aiogram.types import Message

from app.core.config import settings


class AntiFloodMiddleware(BaseMiddleware):

    def __init__(self):
        self.storage: dict = {}

    async def __call__(
        self,
        handler,
        event,
        data
    ):
        if not isinstance(event, Message):
            return await handler(event, data)

        user_id = event.from_user.id

        now = time.time()

        history = self.storage.get(
            user_id,
            []
        )

        history = [
            t for t in history
            if now - t < settings.FLOOD_TIME
        ]

        if len(history) >= settings.FLOOD_LIMIT:
            return

        history.append(now)

        self.storage[user_id] = history

        return await handler(
            event,
            data
        )