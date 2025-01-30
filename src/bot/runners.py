import logging

from aiogram import Bot, Dispatcher, loggers
from aiogram.types import BotCommand

from src.app_config import AppConfig

logger: logging.Logger = logging.getLogger(__name__)


async def set_default_commands(bot: Bot):
    await bot.set_my_commands([BotCommand(command="start", description="Main menu")])


async def admin_notification(text: str, admins: list[int], bot: Bot):
    for admin in admins:
        try:
            await bot.send_message(chat_id=admin, text=text)
        except Exception as e:
            logger.exception(e)


async def polling_startup(bots: list[Bot], config: AppConfig) -> None:
    for bot in bots:
        await bot.delete_webhook(drop_pending_updates=config.common.drop_pending_updates)
        await set_default_commands(bot)
        await admin_notification(text="Bot launched!", admins=config.common.admins, bot=bot)
    if config.common.drop_pending_updates:
        loggers.dispatcher.info("Updates skipped successfully")


def run_polling(dispatcher: Dispatcher, bot: Bot) -> None:
    dispatcher.startup.register(polling_startup)
    return dispatcher.run_polling(bot, allowed_updates=dispatcher.resolve_used_update_types())
