import logging
from typing import Any, Awaitable, Callable

from aiogram import BaseMiddleware
from aiogram.dispatcher.event.bases import UNHANDLED
from aiogram.types import TelegramObject, Update

logger: logging.Logger = logging.getLogger(__name__)


class LogUpdatesMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: dict[str, Any],
    ) -> Any:
        result = await handler(event, data)
        if result == UNHANDLED:
            logger.error(f"Unhandled event: %s", event.model_dump())
        else:
            logger.debug(f"New event: %s", event.model_dump())
        return result
