# bot/handlers/result.py

import os
import json
import logging
from collections import defaultdict

from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.services.media import generate_image  # сервис генерации картинок

router = Router()
logger = logging.getLogger("zoo_totem_bot.result")

# Предварительно загружаем данные о животных
ANIMALS_PATH = os.path.join("data", "animals.json")
with open(ANIMALS_PATH, encoding="utf-8") as f:
    ANIMALS = json.load(f)
logger.info(f"Загружены данные о {len(ANIMALS)} животных")

async def show_result(message: types.Message, state: FSMContext):
    """Формирует и отправляет итоговый результат викторины."""
    data = await state.get_data()
    answers = data.get("answers", [])

    # 1) Подсчёт баллов
    score = defaultdict(int)
    for weight_list in answers:
        for animal in weight_list:
            score[animal] += 1

    if not score:
        await message.answer("⚠️ Не удалось обработать результаты викторины.")
        return

    # 2) Определяем тотема (максимальный балл)
    totem_key = max(score.items(), key=lambda x: x[1])[0]
    animal = ANIMALS.get(totem_key)
    if not animal:
        await message.answer("⚠️ Ваше тотемное животное не найдено в базе.")
        return

    logger.info(f"Пользователь {message.from_user.id} — тотем: {animal['name']} ({score[totem_key]} очков)")

    # 3) Генерируем изображение с логотипом и подписями
    try:
        image_path = await generate_image(
            image_path=animal["image"],
            animal_name=animal["name"],
            user_name=message.from_user.first_name
        )
    except Exception as e:
        logger.exception("Ошибка при генерации итоговой картинки")
        image_path = None

    # 4) Формируем подпись к сообщению
    caption = (
        f"🎉 *Твоё тотемное животное — {animal['name']}!*\n\n"
        f"_{animal['description']}_\n\n"
        f"[Узнать об опеке]({animal['guardian_link']})"
    )

    # 5) Кнопки действия
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔁 Ещё раз", callback_data="start_quiz")],
        [InlineKeyboardButton(text="📢 Поделиться", callback_data=f"share_{totem_key}")],
        [InlineKeyboardButton(text="💬 Отзыв", callback_data="feedback")],
        [InlineKeyboardButton(text="📞 Связаться", callback_data=f"contact_{totem_key}")]
    ])

    # 6) Отправляем результат
    if image_path:
        await message.answer_photo(
            photo=types.FSInputFile(image_path),
            caption=caption,
            parse_mode="Markdown",
            reply_markup=kb
        )
    else:
        # Если картинка не сгенерировалась — только текст
        await message.answer(
            caption,
            parse_mode="Markdown",
            reply_markup=kb
        )

    # 7) Очищаем состояние
    await state.clear()
