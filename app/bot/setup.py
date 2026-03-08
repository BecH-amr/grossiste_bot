from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from app.core.config import settings

bot = Bot(
    token=settings.BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN_V2),
)
dp = Dispatcher()


_handlers_registered = False


def register_handlers() -> None:
    global _handlers_registered
    if _handlers_registered:
        return
    from app.bot.handlers import start, catalog

    dp.include_router(start.router)
    dp.include_router(catalog.router)
    _handlers_registered = True
