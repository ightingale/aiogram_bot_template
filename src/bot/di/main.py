from typing import AsyncIterable

from aiohttp import ClientSession
from dishka import Provider, Scope, provide
from redis.asyncio import Redis

from ..app_config import AppConfig
from ..factory.app_config import create_app_config


class MainProvider(Provider):
    scope = Scope.APP

    @provide
    async def provide_config(self) -> AppConfig:
        return create_app_config()

    @provide
    async def provide_redis(self, config: AppConfig) -> Redis:
        return Redis.from_url(url=config.redis.build_url())

    @provide
    async def provide_aiohttp_session(self) -> AsyncIterable[ClientSession]:
        session = ClientSession()
        try:
            yield session
        finally:
            await session.close()
