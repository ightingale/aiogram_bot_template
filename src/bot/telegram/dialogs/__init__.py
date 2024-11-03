from typing import Final

from aiogram import Router

from . import entrypoint, start

router: Final[Router] = Router(name=__name__)
router.include_routers(
    entrypoint.router,
    start.router,
)
