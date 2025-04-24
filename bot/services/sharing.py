# bot/services/sharing.py

import logging
from aiogram import types

logger = logging.getLogger("zoo_totem_bot.sharing")

async def share_result(message: types.Message, totem_key: str):
    bot_username = message.bot.username or "ZooTotemBot"
    bot_mention = f"@{bot_username.lstrip('@')}"
    text = (
        f"🐾 Я прошёл викторину от Московского зоопарка и узнал, "
        f"что моё тотемное животное — *{totem_key}*!\n\n"
        f"Хочешь узнать, кто ты? → {bot_mention}"
    )
    logger.info(f"share_result: user_id={message.from_user.id}, totem={totem_key}")
    await message.answer(text, parse_mode="Markdown")
