from pydantic import BaseModel, SecretStr
from pydantic_settings import BaseSettings as _BaseSettings
from pydantic_settings import SettingsConfigDict
from sqlalchemy import URL


class BaseSettings(_BaseSettings):
    model_config = SettingsConfigDict(extra="ignore", env_file=".env", env_file_encoding="utf-8")


class CommonConfig(BaseSettings, env_prefix="COMMON_"):
    bot_token: SecretStr
    drop_pending_updates: bool
    sqlalchemy_logging: bool
    admins: list[int]


class PostgresConfig(BaseSettings, env_prefix="POSTGRES_"):
    host: str
    db: str
    password: SecretStr
    port: int
    user: str
    data: str

    def build_dsn(self) -> URL:
        return URL.create(
            drivername="postgresql+asyncpg",
            username=self.user,
            password=self.password.get_secret_value(),
            host=self.host,
            port=self.port,
            database=self.db,
        )


class RedisConfig(BaseSettings, env_prefix="REDIS_"):
    host: str
    password: SecretStr
    port: int
    db: int
    data: str

    def build_url(self) -> str:
        return f"redis://:{self.password.get_secret_value()}@{self.host}:{self.port}/{self.db}"


class AppConfig(BaseModel):
    common: CommonConfig
    postgres: PostgresConfig
    redis: RedisConfig
