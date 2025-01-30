import logging
from typing import Final

from aiogram import Router

logger: logging.Logger = logging.getLogger(__name__)

router: Final[Router] = Router(name=__name__)
