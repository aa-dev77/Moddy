from app.database.database import db


class SettingsService:

    async def set_welcome_text(
        self,
        chat_id: int,
        text: str
    ):
        await db.save_welcome_text(
            chat_id,
            text
        )

    async def set_welcome_photo(
        self,
        chat_id: int,
        photo_id: str
    ):
        await db.save_welcome_photo(
            chat_id,
            photo_id
        )

    async def set_welcome_voice(
        self,
        chat_id: int,
        voice_id: str
    ):
        await db.save_welcome_voice(
            chat_id,
            voice_id
        )

    async def set_exit_text(
        self,
        chat_id: int,
        text: str
    ):
        await db.save_exit_text(
            chat_id,
            text
        )

    async def get_settings(
        self,
        chat_id: int
    ):
        return await db.get_group_settings(
            chat_id
        )


settings_service = SettingsService()