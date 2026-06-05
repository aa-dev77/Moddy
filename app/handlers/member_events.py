from aiogram import Router
from aiogram.types import Message

from app.services.settings_service import (
    settings_service
)

router = Router()


@router.message()
async def new_members_handler(
    message: Message
):
    if not message.new_chat_members:
        return

    settings = (
        await settings_service.get_settings(
            message.chat.id
        )
    )

    if not settings:
        return

    welcome_text = settings[0]
    welcome_photo = settings[1]
    welcome_voice = settings[2]

    for member in message.new_chat_members:

        text = (
            welcome_text
            or f"Xush kelibsiz {member.full_name}"
        )

        if welcome_photo:

            await message.answer_photo(
                photo=welcome_photo,
                caption=text
            )

        elif welcome_voice:

            await message.answer_voice(
                voice=welcome_voice,
                caption=text
            )

        else:

            await message.answer(text)


@router.message()
async def left_member_handler(
    message: Message
):
    if not message.left_chat_member:
        return

    settings = (
        await settings_service.get_settings(
            message.chat.id
        )
    )

    if not settings:
        return

    exit_text = settings[3]

    if exit_text:
        await message.answer(
            exit_text
        )