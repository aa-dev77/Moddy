from aiogram import Bot


async def is_group_admin(
    bot: Bot,
    chat_id: int,
    user_id: int
) -> bool:

    member = await bot.get_chat_member(
        chat_id=chat_id,
        user_id=user_id
    )

    return member.status in (
        "creator",
        "administrator"
    )