from aiogram import Router
from aiogram.types import Message

from app.services.whitelist_service import (
    whitelist_service
)

from app.services.moderation_service import (
    moderation_service
)

from app.utils.validators import (
    contains_advertisement
)

router = Router()


@router.message()
async def security_handler(
    message: Message
):
    if not message.text:
        return

    if message.chat.type == "private":
        return

    user_id = message.from_user.id

    is_allowed = (
        await whitelist_service.is_allowed(
            message.chat.id,
            user_id
        )
    )

    if not is_allowed:

        if contains_advertisement(
            message.text
        ):
            try:
                await message.delete()
            except Exception:
                pass

            return

    has_blacklisted = (
        await moderation_service
        .contains_blacklisted_word(
            message.chat.id,
            message.text
        )
    )

    if has_blacklisted:

        try:
            await message.delete()
        except Exception:
            pass