from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Автоматически берёт значения из .env
    DATABASE_URL: str
    SECRET_KEY: str
    # ALGORITHM: str = "HS256"
    # ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Можно задавать значения по умолчанию
    ENV: str = "development"
    DEBUG: bool = False

    model_config = SettingsConfigDict(
        env_file=".env",              # имя файла
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",               # игнорировать лишние переменные
    )


# Один экземпляр на всё приложение
settings = Settings()