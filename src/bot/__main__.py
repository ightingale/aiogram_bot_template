from aiogram import Bot, Dispatcher

from src.app_config import AppConfig
from src.factory import create_app_config, create_bot, create_dispatcher
from src.bot.runners import run_polling
from src.utils.loggers import setup_logger


def main() -> None:
    setup_logger()
    config: AppConfig = create_app_config()
    dispatcher: Dispatcher = create_dispatcher(config=config)
    bot: Bot = create_bot(config=config)
    return run_polling(dispatcher=dispatcher, bot=bot)


if __name__ == "__main__":
    main()
