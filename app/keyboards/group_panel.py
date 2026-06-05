from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton
)


def group_panel_keyboard():

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="👋 Welcome",
                    callback_data="panel_welcome"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🚪 Exit Text",
                    callback_data="panel_exit"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🛡 Moderation",
                    callback_data="panel_moderation"
                )
            ],
            [
                InlineKeyboardButton(
                    text="📋 Blacklist",
                    callback_data="panel_blacklist"
                )
            ],
            [
                InlineKeyboardButton(
                    text="✅ Whitelist",
                    callback_data="panel_whitelist"
                )
            ]
        ]
    )