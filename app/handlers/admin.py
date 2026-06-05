from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from app.filters.bot_admin import BotAdminFilter
from app.services.admin_service import admin_service

router = Router()


@router.message(
    Command("adminadd"),
    BotAdminFilter()
)
async def admin_add_handler(
    message: Message
):
    if not message.reply_to_message:
        await message.answer(
            "Foydalanuvchiga reply qiling."
        )
        return

    user = message.reply_to_message.from_user

    await admin_service.add_admin(
        user.id,
        user.username
    )

    await message.answer(
        f"✅ {user.full_name} admin qilindi."
    )


@router.message(
    Command("adminremove"),
    BotAdminFilter()
)
async def admin_remove_handler(
    message: Message
):
    if not message.reply_to_message:
        await message.answer(
            "Foydalanuvchiga reply qiling."
        )
        return

    user = message.reply_to_message.from_user

    await admin_service.remove_admin(
        user.id
    )

    await message.answer(
        f"❌ {user.full_name} adminlikdan chiqarildi."
    )


@router.message(
    Command("adminlist"),
    BotAdminFilter()
)
async def admin_list_handler(
    message: Message
):
    admins = await admin_service.get_admins()

    if not admins:
        await message.answer(
            "Adminlar mavjud emas."
        )
        return

    text = "📋 Bot Adminlari\n\n"

    for uid, username in admins:
        text += f"• {username or uid}\n"

    await message.answer(text)