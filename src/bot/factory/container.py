from dishka import AsyncContainer, make_async_container

from src.bot.di import BotProvider, MainProvider, SQLProvider


def container_factory() -> AsyncContainer:
    return make_async_container(MainProvider(), SQLProvider(), BotProvider())
