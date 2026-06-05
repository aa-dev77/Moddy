from app.database.database import db


class AdminService:

    async def add_admin(
        self,
        user_id: int,
        username: str | None
    ):
        await db.add_admin(
            user_id=user_id,
            username=username
        )

    async def remove_admin(
        self,
        user_id: int
    ):
        await db.remove_admin(
            user_id
        )

    async def get_admins(self):
        return await db.get_admins()


admin_service = AdminService()