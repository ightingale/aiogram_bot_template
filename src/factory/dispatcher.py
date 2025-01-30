from aiogram import Dispatcher
from aiogram.filters import ExceptionTypeFilter, ChatMemberUpdatedFilter, JOIN_TRANSITION, \
    LEAVE_TRANSITION
from aiogram.fsm.storage.base import DefaultKeyBuilder
from aiogram.fsm.storage.redis import RedisStorage
from aiogram_dialog import setup_dialogs
from aiogram_dialog.api.exceptions import UnknownIntent, UnknownState
from dishka import AsyncContainer
from dishka.integrations.aiogram import setup_dishka
from redis.asyncio import ConnectionPool, Redis

from ..app_config import AppConfig
from ..middlewares.outer.log import LogUpdatesMiddleware
from ..middlewares.outer.user import UserMiddleware
from ..bot.dialogs import router
from ..bot.errors.on_unknown_intent import on_unknown_intent
from ..bot.utils import switch_notifications
from ..utils import msgspec_json as mjson


def _setup_middlewares(dispatcher: Dispatcher, container: AsyncContainer) -> None:
    dispatcher.update.outer_middleware(LogUpdatesMiddleware())
    dispatcher.update.outer_middleware(UserMiddleware(container=container))


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

    dispatcher.errors.register(on_unknown_intent, ExceptionTypeFilter(UnknownIntent))
    dispatcher.errors.register(on_unknown_intent, ExceptionTypeFilter(UnknownState))

    dispatcher.my_chat_member.register(
        switch_notifications, ChatMemberUpdatedFilter(LEAVE_TRANSITION)
    )
    dispatcher.my_chat_member.register(
        switch_notifications, ChatMemberUpdatedFilter(JOIN_TRANSITION)
    )

    from src.factory.container import container_factory

    container = container_factory(config=config)
    setup_dishka(container=container, router=dispatcher, auto_inject=True)
    setup_dialogs(dispatcher)

    if setup_middlewares:
        _setup_middlewares(dispatcher=dispatcher, container=container)

    return dispatcher
