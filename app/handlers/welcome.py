from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from app.filters.group_admin import GroupAdminFilter
from app.services.settings_service import settings_service

router = Router()


@router.message(
    Command("setwelcome"),
    GroupAdminFilter()
)
async def set_welcome(
    message: Message
):
    if message.photo:

        photo_id = message.photo[-1].file_id

        await settings_service.set_welcome_photo(
            message.chat.id,
            photo_id
        )

        await message.answer(
            "✅ Welcome photo saqlandi."
        )

        return

    if message.voice:

        await settings_service.set_welcome_voice(
            message.chat.id,
            message.voice.file_id
        )

        await message.answer(
            "✅ Welcome voice saqlandi."
        )

        return

    text = message.text.replace(
        "/setwelcome",
        ""
    ).strip()

    if not text:
        await message.answer(
            "Matn yuboring."
        )
        return

    await settings_service.set_welcome_text(
        message.chat.id,
        text
    )

    await message.answer(
        "✅ Welcome text saqlandi."
    )