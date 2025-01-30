from dishka import AsyncContainer, make_async_container

from src.app_config import AppConfig
from src.di import BotProvider, MainProvider, SQLProvider
from src.di.data import DataProvider


def container_factory(config: AppConfig) -> AsyncContainer:
    return make_async_container(
        MainProvider(),
        SQLProvider(),
        BotProvider(),
        DataProvider(),
        context={
            AppConfig: config
        }
    )
