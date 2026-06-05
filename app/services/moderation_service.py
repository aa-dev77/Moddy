from app.database.database import db


class ModerationService:

    async def add_blacklist_word(
        self,
        chat_id: int,
        word: str
    ):
        await db.add_blacklist_word(
            chat_id,
            word
        )

    async def get_blacklist(
        self,
        chat_id: int
    ):
        return await db.get_blacklist_words(
            chat_id
        )

    async def contains_blacklisted_word(
        self,
        chat_id: int,
        text: str
    ) -> bool:

        words = await db.get_blacklist_words(
            chat_id
        )

        text = text.lower()

        for word in words:
            if word in text:
                return True

        return False


moderation_service = ModerationService()