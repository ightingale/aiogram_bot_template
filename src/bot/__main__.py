from aiogram import Bot, Dispatcher
from dishka.integrations.aiogram import setup_dishka

from src.bot.app_config import AppConfig
from src.bot.factory import create_app_config, create_bot, create_dispatcher
from src.bot.factory.container import container_factory
from src.bot.runners import run_polling
from src.bot.utils.loggers import setup_logger


def main() -> None:
    setup_logger()
    container = container_factory()
    config: AppConfig = create_app_config()
    dispatcher: Dispatcher = create_dispatcher(config=config)
    bot: Bot = create_bot(config=config)
    setup_dishka(container=container, router=dispatcher)
    return run_polling(dispatcher=dispatcher, bot=bot)


if __name__ == "__main__":
    main()
