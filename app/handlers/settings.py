from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from app.filters.group_admin import GroupAdminFilter
from app.services.settings_service import settings_service
from app.keyboards.group_panel import (
    group_panel_keyboard
)

router = Router()


@router.message(
    Command("grouppanel"),
    GroupAdminFilter()
)
async def group_panel(
    message: Message
):
    await message.answer(
        "⚙ Guruh sozlamalari",
        reply_markup=group_panel_keyboard()
    )


@router.message(
    Command("setexittext"),
    GroupAdminFilter()
)
async def set_exit_text(
    message: Message
):
    args = message.text.replace(
        "/setexittext",
        ""
    ).strip()

    if not args:
        await message.answer(
            "Matn kiriting."
        )
        return

    await settings_service.set_exit_text(
        message.chat.id,
        args
    )

    await message.answer(
        "✅ Exit text saqlandi."
    )