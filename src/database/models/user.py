from typing import Optional, Self

from aiogram import html
from aiogram.enums import ChatType
from aiogram.types import Chat, User
from aiogram.utils.link import create_tg_link
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base, Int64, TimestampMixin


class DBUser(Base, TimestampMixin):
    __tablename__ = "users"

    id: Mapped[Int64] = mapped_column(primary_key=True, nullable=False)
    name: Mapped[str] = mapped_column(nullable=False)
    username: Mapped[Optional[str]]
    notifications: Mapped[bool] = mapped_column(default=False, nullable=False)

    @property
    def url(self) -> str:
        return create_tg_link("user", id=self.id)

    @property
    def mention(self) -> str:
        return html.paid(value=self.name, link=self.url)

    @classmethod
    def from_aiogram(cls, user: User, chat: Chat) -> Self:
        return cls(
            id=user.id,
            name=user.full_name,
            username=user.username,
            notifications=chat.type == ChatType.PRIVATE,
        )

    def enable_notifications(self) -> None:
        self.notifications = True  # noqa: F841

    def disable_notifications(self) -> None:
        self.notifications = False  # noqa: F841
