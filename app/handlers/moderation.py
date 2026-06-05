from datetime import datetime
from datetime import timedelta

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.types import ChatPermissions

from app.filters.group_admin import GroupAdminFilter
from app.services.moderation_service import moderation_service
from app.utils.parser import parse_duration

router = Router()


@router.message(
    Command("mute"),
    GroupAdminFilter()
)
async def mute_handler(
    message: Message
):
    if not message.reply_to_message:
        return

    command = message.text.split()

    if len(command) < 2:
        await message.answer(
            "Masalan: /mute 10m"
        )
        return

    seconds = parse_duration(
        command[1]
    )

    if not seconds:
        return

    until_date = datetime.now() + timedelta(
        seconds=seconds
    )

    await message.bot.restrict_chat_member(
        chat_id=message.chat.id,
        user_id=message.reply_to_message.from_user.id,
        permissions=ChatPermissions(),
        until_date=until_date
    )

    await message.answer(
        "🔇 Mutega tushirildi."
    )


@router.message(
    Command("unmute"),
    GroupAdminFilter()
)
async def unmute_handler(
    message: Message
):
    if not message.reply_to_message:
        return

    await message.bot.restrict_chat_member(
        chat_id=message.chat.id,
        user_id=message.reply_to_message.from_user.id,
        permissions=ChatPermissions(
            can_send_messages=True,
            can_send_other_messages=True,
            can_send_audios=True,
            can_send_documents=True,
            can_send_photos=True,
            can_send_videos=True
        )
    )

    await message.answer(
        "✅ Unmute qilindi."
    )


@router.message(
    Command("ban"),
    GroupAdminFilter()
)
async def ban_handler(
    message: Message
):
    if not message.reply_to_message:
        return

    await message.bot.ban_chat_member(
        message.chat.id,
        message.reply_to_message.from_user.id
    )

    await message.answer(
        "⛔ Ban qilindi."
    )


@router.message(
    Command("unban"),
    GroupAdminFilter()
)
async def unban_handler(
    message: Message
):
    if not message.reply_to_message:
        return

    await message.bot.unban_chat_member(
        message.chat.id,
        message.reply_to_message.from_user.id
    )

    await message.answer(
        "✅ Unban qilindi."
    )


@router.message(
    Command("kick"),
    GroupAdminFilter()
)
async def kick_handler(
    message: Message
):
    if not message.reply_to_message:
        return

    uid = message.reply_to_message.from_user.id

    await message.bot.ban_chat_member(
        message.chat.id,
        uid
    )

    await message.bot.unban_chat_member(
        message.chat.id,
        uid
    )

    await message.answer(
        "👢 Kick qilindi."
    )


@router.message(
    Command("addblacklist"),
    GroupAdminFilter()
)
async def add_blacklist(
    message: Message
):
    text = message.text.replace(
        "/addblacklist",
        ""
    ).strip()

    if not text:
        return

    await moderation_service.add_blacklist_word(
        message.chat.id,
        text
    )

    await message.answer(
        "✅ So'z qo'shildi."
    )


@router.message(
    Command("blacklist"),
    GroupAdminFilter()
)
async def blacklist_list(
    message: Message
):
    words = await moderation_service.get_blacklist(
        message.chat.id
    )

    if not words:
        await message.answer(
            "Ro'yxat bo'sh."
        )
        return

    text = "🚫 Blacklist:\n\n"

    for word in words:
        text += f"• {word}\n"

    await message.answer(text)