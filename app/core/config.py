from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    BOT_TOKEN: str
    SECRET_TOKEN: str  # required — generate with: python -c "import secrets; print(secrets.token_urlsafe(32))"
    WEBHOOK_URL: str = ""
    DB_URL: str = "sqlite+aiosqlite:///./catalog.db"
    USE_POLLING: bool = True

    CONTACT_SNAPCHAT: str = "@your_snapchat"


settings = Settings()
