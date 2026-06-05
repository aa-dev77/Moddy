from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from app.filters.group_admin import GroupAdminFilter
from app.services.whitelist_service import whitelist_service

router = Router()


@router.message(
    Command("whitelistuser"),
    GroupAdminFilter()
)
async def whitelist_add(
    message: Message
):
    if not message.reply_to_message:
        await message.answer(
            "Reply ishlating."
        )
        return

    user = message.reply_to_message.from_user

    await whitelist_service.add_user(
        message.chat.id,
        user.id,
        user.username
    )

    await message.answer(
        "✅ Oq ro'yxatga qo'shildi."
    )


@router.message(
    Command("unwhitelistuser"),
    GroupAdminFilter()
)
async def whitelist_remove(
    message: Message
):
    if not message.reply_to_message:
        await message.answer(
            "Reply ishlating."
        )
        return

    user = message.reply_to_message.from_user

    await whitelist_service.remove_user(
        message.chat.id,
        user.id
    )

    await message.answer(
        "❌ Oq ro'yxatdan chiqarildi."
    )