import asyncio

from aiogram import Bot, Dispatcher

from bot.handlers.quiz import router as quiz_router
from bot.handlers.start import router as start_router
from bot.handlers.upload import router as upload_router
from config import BOT_TOKEN
from bot.handlers.stats import router as stats_router
from bot.handlers.repeat import router as repeat_router
from bot.handlers.definitions import router as definitions_router

async def main() -> None:
    """
    Запускает Telegram-бота.
    """
    bot = Bot(token=BOT_TOKEN)
    dispatcher = Dispatcher()

    dispatcher.include_router(start_router)
    dispatcher.include_router(upload_router)
    dispatcher.include_router(quiz_router)
    dispatcher.include_router(stats_router)
    dispatcher.include_router(repeat_router)
    dispatcher.include_router(definitions_router)

    await dispatcher.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())