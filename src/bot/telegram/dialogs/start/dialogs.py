import logging

from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Const

from src.bot.telegram.dialogs.states import MainMenuSG

logger: logging.Logger = logging.getLogger(__name__)

main_menu_dialog = Dialog(Window(Const(text="<b>Main Menu</b>"), state=MainMenuSG.main_menu))
