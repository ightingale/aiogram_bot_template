import logging

from sqlalchemy.ext.asyncio import AsyncSession

logger: logging.Logger = logging.getLogger(__name__)


class _DBInteractor:
    def __init__(self, session: AsyncSession):
        self.session = session
