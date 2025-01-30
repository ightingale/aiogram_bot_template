import logging

from aiogram.types import User
from sqlalchemy import select

from src.domain.db._base import _DBInteractor
from src.database import DBUser

logger: logging.Logger = logging.getLogger(__name__)


class UserNotificationEditor(_DBInteractor):
    async def __call__(self, user: DBUser) -> None:
        user.notifications = not user.notifications
        self.session.add(user)
        await self.session.commit()


class UserGetter(_DBInteractor):
    async def __call__(self, user_id: int) -> DBUser:
        return await self.session.scalar(select(DBUser).where(DBUser.id == user_id))


class UserCreator(_DBInteractor):
    async def __call__(self, user: DBUser) -> None:
        self.session.add(user)
        await self.session.commit()


class UserUpdater(_DBInteractor):
    async def __call__(self, user: DBUser, aiogram_user: User) -> None:
        updated = False

        updated |= self._update_field(user, 'username', aiogram_user.username)
        updated |= self._update_field(user, 'name', aiogram_user.full_name)

        if updated:
            self.session.add(user)
            await self.session.commit()

    @staticmethod
    def _update_field(user: DBUser, field_name: str, new_value: str | None):
        if getattr(user, field_name) != new_value:
            setattr(user, field_name, new_value)
            return True
        return False
