import logging
from typing import AsyncIterable

from aiogram import Bot, Dispatcher
from dishka import Provider, Scope, provide

from src.app_config import AppConfig
from src.domain.db.user import UserNotificationEditor
from src.factory import create_bot, create_dispatcher

logger: logging.Logger = logging.getLogger(__name__)


class BotProvider(Provider):
    scope = Scope.REQUEST
    notifications_editor = provide(UserNotificationEditor)

    @provide(scope=Scope.APP)
    async def provide_dispatcher(self, config: AppConfig) -> Dispatcher:
        return create_dispatcher(config=config, setup_middlewares=False)

    @provide(scope=Scope.APP)
    async def provide_bot(self, config: AppConfig) -> AsyncIterable[Bot]:
        bot = create_bot(config=config)
        try:
            yield bot
        finally:
            await bot.session.close()
