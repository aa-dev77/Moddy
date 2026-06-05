from aiogram.filters import BaseFilter
from aiogram.types import Message

from app.utils.permissions import is_group_admin


class GroupAdminFilter(BaseFilter):

    async def __call__(
        self,
        message: Message
    ) -> bool:

        if not message.from_user:
            return False

        return await is_group_admin(
            bot=message.bot,
            chat_id=message.chat.id,
            user_id=message.from_user.id
        )