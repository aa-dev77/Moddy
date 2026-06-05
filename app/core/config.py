from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    BOT_TOKEN: str

    WEBHOOK_URL: str
    WEBHOOK_SECRET: str

    DATABASE_PATH: str

    BOT_OWNER_ID: int

    FLOOD_LIMIT: int
    FLOOD_TIME: int

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )


settings = Settings()