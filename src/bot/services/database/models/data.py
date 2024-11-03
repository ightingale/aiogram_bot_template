import logging

from sqlalchemy.orm import Mapped, mapped_column

from .base import Base

logger: logging.Logger = logging.getLogger(__name__)


class BotData(Base):
    __tablename__ = "bot_data"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    value: Mapped[str]
