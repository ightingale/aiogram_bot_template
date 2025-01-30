import logging

from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Const

from src.bot.states import AdminMenuSG

logger: logging.Logger = logging.getLogger(__name__)

main_menu_dialog = Dialog(Window(Const(text="<b>Admin Menu</b>"), state=AdminMenuSG.start))
