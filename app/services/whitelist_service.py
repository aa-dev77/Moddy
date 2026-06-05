from app.database.database import db


class WhiteListService:

    async def add_user(
        self,
        chat_id: int,
        user_id: int,
        username: str | None
    ):
        await db.add_whitelist_user(
            chat_id,
            user_id,
            username
        )

    async def remove_user(
        self,
        chat_id: int,
        user_id: int
    ):
        await db.remove_whitelist_user(
            chat_id,
            user_id
        )

    async def is_allowed(
        self,
        chat_id: int,
        user_id: int
    ) -> bool:

        return await db.is_whitelisted(
            chat_id,
            user_id
        )


whitelist_service = WhiteListService()