from typing import Final

from aiogram import F, Router
from aiogram.filters import CommandObject, CommandStart
from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager, StartMode
from dishka import FromDishka
from dishka.integrations.aiogram import inject

from src.bot.services.database import DBUser
from src.bot.telegram.dialogs.states import MainMenuSG

router: Final[Router] = Router(name=__name__)


@router.callback_query(F.data == "main_menu")
async def start(
    _: CallbackQuery,
    dialog_manager: DialogManager,
):
    await dialog_manager.start(state=MainMenuSG.main_menu, mode=StartMode.RESET_STACK)


@router.message(CommandStart(deep_link=True))
@inject
async def start_deep_link(
    _: Message,
    __: CommandObject,
    dialog_manager: DialogManager,
    user: FromDishka[DBUser]
):
    await dialog_manager.start(state=MainMenuSG.main_menu, mode=StartMode.RESET_STACK)


@router.message(CommandStart())
@inject
async def start(
    _: Message,
    dialog_manager: DialogManager,
    user: FromDishka[DBUser]
):
    await dialog_manager.start(state=MainMenuSG.main_menu, mode=StartMode.RESET_STACK)
