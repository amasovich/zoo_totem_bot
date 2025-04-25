# bot/main.py

import sys
import asyncio
import os

# === На Windows переключаем цикл событий на SelectorEventLoop ===
if sys.platform.startswith("win"):
    from asyncio import WindowsSelectorEventLoopPolicy
    asyncio.set_event_loop_policy(WindowsSelectorEventLoopPolicy())
# =============================================================

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv

from utils.logger import setup_logger
from bot.router import router

# 1. Загрузка и проверка токена из .env
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise RuntimeError("Отсутствует переменная окружения BOT_TOKEN в файле .env")

# 2. Настройка логгера
logger = setup_logger("zoo_totem_bot")
logger.info("🚀 Запуск ZooTotemBot…")

async def main():
    # 3. Инициализация бота и диспетчера
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)

    try:
        # 4. Запуск поллинга Telegram
        await dp.start_polling(bot)
    except Exception:
        logger.exception("❌ Неожиданная ошибка в работе бота")
    finally:
        # 5. Закрываем HTTP-сессию бота
        await bot.session.close()
        logger.info("🛑 Бот остановлен")

if __name__ == "__main__":
    # 6. Запускаем главный корутин через asyncio
    asyncio.run(main())
