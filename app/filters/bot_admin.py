from aiogram.filters import BaseFilter
from aiogram.types import Message

from app.database.database import db
from app.core.config import settings


class BotAdminFilter(BaseFilter):

    async def __call__(
        self,
        message: Message
    ) -> bool:

        if not message.from_user:
            return False

        if message.from_user.id == settings.BOT_OWNER_ID:
            return True

        return await db.is_admin(
            message.from_user.id
        )