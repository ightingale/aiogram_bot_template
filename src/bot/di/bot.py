import logging
from typing import AsyncIterable

from aiogram import Bot, Dispatcher
from aiogram.types import CallbackQuery, Message, TelegramObject
from dishka import Provider, Scope, from_context, provide
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.bot.app_config import AppConfig
from src.bot.factory import create_bot, create_dispatcher
from src.bot.services.database import DBUser

logger: logging.Logger = logging.getLogger(__name__)


class BotProvider(Provider):
    scope = Scope.REQUEST
    call = from_context(provides=TelegramObject, scope=Scope.REQUEST)

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

    @provide
    async def get_user(self, session: AsyncSession, call: TelegramObject) -> DBUser:
        call: Message | CallbackQuery
        user: DBUser = await session.scalar(select(DBUser).where(DBUser.id == call.from_user.id))
        if not user:
            user = DBUser.from_aiogram(user=call.from_user, chat=call.chat)
            session.add(user)
            await session.commit()
        return user
