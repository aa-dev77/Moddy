import aiosqlite

from app.core.config import settings


class Database:
    def __init__(self):
        self.db_path = settings.DATABASE_PATH

    async def connect(self):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("PRAGMA foreign_keys = ON;")
            await db.commit()

    async def create_tables(self):
        async with aiosqlite.connect(self.db_path) as db:

            await db.execute("""
            CREATE TABLE IF NOT EXISTS bot_admins (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL UNIQUE,
                username TEXT
            )
            """)

            await db.execute("""
            CREATE TABLE IF NOT EXISTS group_settings (
                chat_id INTEGER PRIMARY KEY,

                welcome_text TEXT,
                welcome_photo TEXT,
                welcome_voice TEXT,

                exit_text TEXT
            )
            """)

            await db.execute("""
            CREATE TABLE IF NOT EXISTS whitelist_users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,

                chat_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                username TEXT,

                UNIQUE(chat_id, user_id)
            )
            """)

            await db.execute("""
            CREATE TABLE IF NOT EXISTS blacklist_words (
                id INTEGER PRIMARY KEY AUTOINCREMENT,

                chat_id INTEGER NOT NULL,
                word TEXT NOT NULL,

                UNIQUE(chat_id, word)
            )
            """)

            await db.commit()

    # ==========================
    # BOT ADMINS
    # ==========================

    async def add_admin(
        self,
        user_id: int,
        username: str | None
    ):
        async with aiosqlite.connect(self.db_path) as db:

            await db.execute(
                """
                INSERT OR IGNORE INTO bot_admins
                (user_id, username)
                VALUES (?, ?)
                """,
                (
                    user_id,
                    username
                )
            )

            await db.commit()

    async def remove_admin(
        self,
        user_id: int
    ):
        async with aiosqlite.connect(self.db_path) as db:

            await db.execute(
                """
                DELETE FROM bot_admins
                WHERE user_id = ?
                """,
                (user_id,)
            )

            await db.commit()

    async def is_admin(
        self,
        user_id: int
    ) -> bool:

        async with aiosqlite.connect(self.db_path) as db:

            cursor = await db.execute(
                """
                SELECT user_id
                FROM bot_admins
                WHERE user_id = ?
                """,
                (user_id,)
            )

            row = await cursor.fetchone()

            return row is not None

    async def get_admins(self):
        async with aiosqlite.connect(self.db_path) as db:

            cursor = await db.execute(
                """
                SELECT user_id, username
                FROM bot_admins
                ORDER BY id
                """
            )

            return await cursor.fetchall()

    # ==========================
    # GROUP SETTINGS
    # ==========================

    async def save_welcome_text(
        self,
        chat_id: int,
        text: str
    ):
        async with aiosqlite.connect(self.db_path) as db:

            await db.execute(
                """
                INSERT INTO group_settings
                (chat_id, welcome_text)

                VALUES (?, ?)

                ON CONFLICT(chat_id)
                DO UPDATE SET
                welcome_text = excluded.welcome_text
                """,
                (
                    chat_id,
                    text
                )
            )

            await db.commit()

    async def save_welcome_photo(
        self,
        chat_id: int,
        photo_id: str
    ):
        async with aiosqlite.connect(self.db_path) as db:

            await db.execute(
                """
                INSERT INTO group_settings
                (chat_id, welcome_photo)

                VALUES (?, ?)

                ON CONFLICT(chat_id)
                DO UPDATE SET
                welcome_photo = excluded.welcome_photo
                """,
                (
                    chat_id,
                    photo_id
                )
            )

            await db.commit()

    async def save_welcome_voice(
        self,
        chat_id: int,
        voice_id: str
    ):
        async with aiosqlite.connect(self.db_path) as db:

            await db.execute(
                """
                INSERT INTO group_settings
                (chat_id, welcome_voice)

                VALUES (?, ?)

                ON CONFLICT(chat_id)
                DO UPDATE SET
                welcome_voice = excluded.welcome_voice
                """,
                (
                    chat_id,
                    voice_id
                )
            )

            await db.commit()

    async def save_exit_text(
        self,
        chat_id: int,
        text: str
    ):
        async with aiosqlite.connect(self.db_path) as db:

            await db.execute(
                """
                INSERT INTO group_settings
                (chat_id, exit_text)

                VALUES (?, ?)

                ON CONFLICT(chat_id)
                DO UPDATE SET
                exit_text = excluded.exit_text
                """,
                (
                    chat_id,
                    text
                )
            )

            await db.commit()

    async def get_group_settings(
        self,
        chat_id: int
    ):
        async with aiosqlite.connect(self.db_path) as db:

            cursor = await db.execute(
                """
                SELECT
                    welcome_text,
                    welcome_photo,
                    welcome_voice,
                    exit_text
                FROM group_settings
                WHERE chat_id = ?
                """,
                (chat_id,)
            )

            return await cursor.fetchone()

    # ==========================
    # WHITELIST
    # ==========================

    async def add_whitelist_user(
        self,
        chat_id: int,
        user_id: int,
        username: str | None
    ):
        async with aiosqlite.connect(self.db_path) as db:

            await db.execute(
                """
                INSERT OR IGNORE INTO whitelist_users
                (chat_id, user_id, username)

                VALUES (?, ?, ?)
                """,
                (
                    chat_id,
                    user_id,
                    username
                )
            )

            await db.commit()

    async def remove_whitelist_user(
        self,
        chat_id: int,
        user_id: int
    ):
        async with aiosqlite.connect(self.db_path) as db:

            await db.execute(
                """
                DELETE FROM whitelist_users
                WHERE chat_id = ?
                AND user_id = ?
                """,
                (
                    chat_id,
                    user_id
                )
            )

            await db.commit()

    async def is_whitelisted(
        self,
        chat_id: int,
        user_id: int
    ) -> bool:

        async with aiosqlite.connect(self.db_path) as db:

            cursor = await db.execute(
                """
                SELECT user_id
                FROM whitelist_users
                WHERE chat_id = ?
                AND user_id = ?
                """,
                (
                    chat_id,
                    user_id
                )
            )

            row = await cursor.fetchone()

            return row is not None

    # ==========================
    # BLACKLIST WORDS
    # ==========================

    async def add_blacklist_word(
        self,
        chat_id: int,
        word: str
    ):
        async with aiosqlite.connect(self.db_path) as db:

            await db.execute(
                """
                INSERT OR IGNORE INTO blacklist_words
                (chat_id, word)

                VALUES (?, ?)
                """,
                (
                    chat_id,
                    word.lower()
                )
            )

            await db.commit()

    async def get_blacklist_words(
        self,
        chat_id: int
    ):
        async with aiosqlite.connect(self.db_path) as db:

            cursor = await db.execute(
                """
                SELECT word
                FROM blacklist_words
                WHERE chat_id = ?
                ORDER BY word
                """,
                (chat_id,)
            )

            rows = await cursor.fetchall()

            return [row[0] for row in rows]


db = Database()