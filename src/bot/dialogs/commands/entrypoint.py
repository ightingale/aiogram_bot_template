from typing import Final

from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode

from src.bot.states import MainMenuSG

router: Final[Router] = Router(name=__name__)


@router.message(CommandStart())
async def start(_: Message, dialog_manager: DialogManager):
    await dialog_manager.start(state=MainMenuSG.start, mode=StartMode.RESET_STACK)
