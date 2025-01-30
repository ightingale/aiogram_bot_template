from typing import Final

from aiogram import Router

from .dialogs import main_menu_dialog

router: Final[Router] = Router(name=__name__)
router.include_routers(main_menu_dialog)
