import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from config import config
from database.db import async_session, init_db
from database.requests import ensure_default_prices
from handlers import admin, common, user
from middlewares.db_middleware import DbSessionMiddleware
from middlewares.logging_middleware import ActionLoggingMiddleware
from utils.logger import logger


async def main() -> None:
    if not config.BOT_TOKEN or not config.SUPER_ADMIN_ID:
        raise RuntimeError("BOT_TOKEN не задан. Проверьте файл .env")

    await init_db()
    async with async_session() as session:
        await ensure_default_prices(session)

    bot = Bot(token=config.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher(storage=MemoryStorage())

    # Middleware вешаем отдельно на message и callback_query (а не на
    # верхнеуровневый update), чтобы data["event_from_user"] уже был
    # заполнен встроенным UserContextMiddleware aiogram.
    dp.message.outer_middleware(DbSessionMiddleware())
    dp.message.outer_middleware(ActionLoggingMiddleware())
    dp.callback_query.outer_middleware(DbSessionMiddleware())
    dp.callback_query.outer_middleware(ActionLoggingMiddleware())

    dp.include_router(common.router)
    dp.include_router(admin.router)
    dp.include_router(user.router)

    logger.info("Bot started")
    await bot.delete_webhook(drop_pending_updates=True)
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped")
