# bot/handlers/sharing.py

import logging
from aiogram import Router, F

from bot.services.sharing import share_result

router = Router()
logger = logging.getLogger("zoo_totem_bot.sharing")

@router.callback_query(F.data.startswith("share_"))
async def share_callback(callback: types.CallbackQuery):
    totem_key = callback.data.replace("share_", "")
    logger.info(f"Пользователь {callback.from_user.id} делится результатом: {totem_key}")
    await share_result(callback.message, totem_key)
    await callback.answer()