import logging

from aiogram.exceptions import TelegramBadRequest
from aiogram.types import ErrorEvent
from aiogram_dialog import DialogManager, ShowMode, StartMode

from src.bot.states import MainMenuSG

logger: logging.Logger = logging.getLogger(__name__)


async def on_unknown_intent(event: ErrorEvent, dialog_manager: DialogManager):
    logging.error("Restarting dialog: %s", event.exception)
    if event.update.callback_query:
        if event.update.callback_query.message:
            try:  # noqa: SIM105
                await event.update.callback_query.message.delete()
            except TelegramBadRequest:
                pass
    await dialog_manager.start(
        state=MainMenuSG.start,
        mode=StartMode.RESET_STACK,
        show_mode=ShowMode.SEND,
    )
