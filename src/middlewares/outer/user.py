import logging
from typing import Any, Awaitable, Callable, Optional

from aiogram import BaseMiddleware
from aiogram.types import Chat, TelegramObject, User
from dishka import AsyncContainer

from src.app_config import AppConfig
from src.database import DBUser
from src.domain.db.user import UserGetter, UserCreator, UserUpdater

logger: logging.Logger = logging.getLogger(__name__)


class UserMiddleware(BaseMiddleware):
    def __init__(self, container: AsyncContainer):
        self.container = container

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Optional[Any]:
        aiogram_user: Optional[User] = data.get("event_from_user")
        chat: Optional[Chat] = data.get("event_chat")
        if aiogram_user is None or chat is None or aiogram_user.is_bot:
            return await handler(event, data)

        async with self.container() as sub_container:
            get_user = await sub_container.get(UserGetter)
            user: Optional[DBUser] = await get_user(user_id=aiogram_user.id)
            config = await sub_container.get(AppConfig)

        if user is None:
            user = DBUser.from_aiogram(
                user=aiogram_user,
                chat=chat,
            )

            async with self.container() as sub_container:
                create_user = await sub_container.get(UserCreator)
                await create_user(user=user)

            logger.info("New user in database: %s (%d)", aiogram_user.full_name, aiogram_user.id)
            data["new_user"] = True
        else:
            async with self.container() as sub_container:
                update_user = await sub_container.get(UserUpdater)
                await update_user(user=user, aiogram_user=aiogram_user)

        data["user"] = user
        data["admin"] = user.id in config.common.admins

        return await handler(event, data)
