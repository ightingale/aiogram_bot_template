from aiogram import Dispatcher
from aiogram.fsm.storage.base import DefaultKeyBuilder
from aiogram.fsm.storage.redis import RedisStorage
from aiogram_dialog import setup_dialogs
from redis.asyncio import ConnectionPool, Redis

from ..app_config import AppConfig
from ..middlewares.outer.log import LogUpdatesMiddleware
from ..telegram.dialogs import router
from ..utils import msgspec_json as mjson


def _setup_outer_middlewares(dispatcher: Dispatcher) -> None:
    dispatcher.update.outer_middleware(LogUpdatesMiddleware())


def create_dispatcher(config: AppConfig, setup_middlewares: bool = True) -> Dispatcher:
    """
    :return: Configured ``Dispatcher`` with installed middlewares and included routers
    """
    redis: Redis = Redis(connection_pool=ConnectionPool.from_url(url=config.redis.build_url()))

    dispatcher: Dispatcher = Dispatcher(
        name="main_dispatcher",
        storage=RedisStorage(
            redis=redis,
            json_loads=mjson.decode,
            json_dumps=mjson.encode,
            key_builder=DefaultKeyBuilder(with_destiny=True),
        ),
        config=config,
    )

    dispatcher.include_routers(router)
    setup_dialogs(dispatcher)

    if setup_middlewares:
        _setup_outer_middlewares(dispatcher=dispatcher)

    return dispatcher
