from typing import Final

from aiogram import Router

from . import start, commands, admin

router: Final[Router] = Router(name=__name__)
router.include_routers(
    start.router,
    commands.router,
    admin.router,
)
