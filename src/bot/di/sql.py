import logging
from typing import AsyncIterable

from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from src.bot.app_config import AppConfig

logger: logging.Logger = logging.getLogger(__name__)


class SQLProvider(Provider):
    @provide(scope=Scope.APP)
    def provide_engine(self, config: AppConfig) -> AsyncEngine:
        return create_async_engine(
            config.postgres.build_dsn(),
            pool_size=10,
            max_overflow=0,
            pool_pre_ping=True,
            connect_args={
                "timeout": 15,
                "command_timeout": 5,
                "server_settings": {
                    "jit": "off",
                    "application_name": "bot",
                },
            },
        )

    @provide(scope=Scope.APP)
    def provide_sessionmaker(
        self,
        engine: AsyncEngine,
    ) -> async_sessionmaker[AsyncSession]:
        return async_sessionmaker(bind=engine, expire_on_commit=False)

    @provide(scope=Scope.REQUEST, provides=AsyncSession)
    async def provide_session(
        self, sessionmaker: async_sessionmaker[AsyncSession]
    ) -> AsyncIterable[AsyncSession]:
        async with sessionmaker() as session:
            yield session
