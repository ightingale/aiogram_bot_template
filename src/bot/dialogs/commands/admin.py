from typing import Final

from aiogram import F, Router
from aiogram.filters import Command, MagicData
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode

from src.bot.states import AdminMenuSG

router: Final[Router] = Router(name=__name__)
router.message.filter(MagicData(F.admin))


@router.message(Command("admin"))
async def admin_command(_: Message, dialog_manager: DialogManager) -> None:
    await dialog_manager.start(state=AdminMenuSG.start, mode=StartMode.RESET_STACK)
