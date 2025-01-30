from typing import AsyncIterable

from aiohttp import ClientSession
from dishka import Provider, Scope, provide, from_context
from redis.asyncio import Redis

from ..app_config import AppConfig


class MainProvider(Provider):
    scope = Scope.APP
    app_config = from_context(AppConfig)

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
