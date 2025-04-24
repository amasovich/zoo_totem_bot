# bot/main.py

import asyncio
import os
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv

from bot.router import router
from utils.logger import setup_logger

# 1. Загрузка и проверка токена
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise RuntimeError("Отсутствует переменная окружения BOT_TOKEN в файле .env")

# 2. Настройка логгера
logger = setup_logger("zoo_totem_bot")

async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)

    try:
        logger.info("🚀 Запуск ZooTotemBot…")
        # Запуск поллинга
        await dp.start_polling(bot)
    except Exception:
        logger.exception("❌ Неожиданная ошибка в работе бота")
    finally:
        # Закрываем сессию HTTP-клиента
        await bot.session.close()
        logger.info("🛑 Бот остановлен")

if __name__ == "__main__":
    # Запускаем главный корутин через asyncio
    asyncio.run(main())