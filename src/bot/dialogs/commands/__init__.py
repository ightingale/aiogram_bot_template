from typing import Final

from aiogram import Router

from . import entrypoint, user, admin

router: Final[Router] = Router(name=__name__)

router.include_routers(entrypoint.router, user.router, admin.router)
