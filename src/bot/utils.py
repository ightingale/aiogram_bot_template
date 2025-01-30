import logging

from aiogram.types import ChatMemberUpdated
from dishka import FromDishka
from dishka.integrations.aiogram import inject

from src.database import DBUser
from src.domain.db.user import UserNotificationEditor

logger: logging.Logger = logging.getLogger(__name__)


@inject
async def switch_notifications(
    _: ChatMemberUpdated,
    user: DBUser,
    edit_notifications: FromDishka[UserNotificationEditor],
) -> None:
    await edit_notifications(user=user)
