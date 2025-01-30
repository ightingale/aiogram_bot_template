import logging

from dishka import Provider, Scope, provide_all

from src.domain.db.user import UserNotificationEditor, UserGetter, UserCreator, UserUpdater

logger: logging.Logger = logging.getLogger(__name__)


class DataProvider(Provider):
    scope = Scope.REQUEST

    all = provide_all(
        UserNotificationEditor,
        UserGetter,
        UserCreator,
        UserUpdater,
    )
