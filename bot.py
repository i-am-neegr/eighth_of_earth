import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.client.session.aiohttp import AiohttpSession
from aiohttp_socks import ProxyConnector

from config import BOT_TOKEN
from database import engine, Base

# ====================== ПРОКСИ ======================
PROXY_URL = "socks5://127.0.0.1:2080"   # ← твой порт из Throne
# ===================================================

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

async def main():
    logging.basicConfig(level=logging.INFO)

    print(f"🔗 Используется прокси: {PROXY_URL}")

    # Создаём прокси-коннектор
    connector = ProxyConnector.from_url(PROXY_URL)

    # Правильный способ для новых версий aiogram
    session = AiohttpSession(proxy=PROXY_URL)

    bot = Bot(
        token=BOT_TOKEN,
        session=session,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )

    # Инициализация базы данных
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        print("✅ База данных готова")
    except Exception as e:
        print(f"⚠️ Ошибка базы данных: {e}")

    dp = Dispatcher()

    # Подключаем хендлеры
    from handlers import start, films, hero, support, premiere, partner

    dp.include_router(start.router)
    dp.include_router(films.router)
    dp.include_router(hero.router)
    dp.include_router(support.router)
    dp.include_router(premiere.router)
    dp.include_router(partner.router)

    print("🚀 Бот запущен через Throne (VLESS)")
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    asyncio.run(main())