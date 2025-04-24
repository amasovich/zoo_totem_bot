# bot/services/media.py

import os
import logging
from PIL import Image, ImageDraw, ImageFont

logger = logging.getLogger("zoo_totem_bot.media")

async def generate_image(
    image_path: str,
    animal_name: str,
    user_name: str
) -> str:
    """
    Открывает исходную картинку animal_name из image_path,
    рисует текст (animal_name и user_name), вставляет логотип
    и сохраняет результат в media/generated/<user>_<animal>.png.
    Возвращает путь к сохранённому файлу.
    """
    # 1) Загружаем основное изображение
    try:
        base = Image.open(image_path).convert("RGBA")
    except Exception:
        logger.exception(f"Не удалось открыть изображение {image_path}")
        raise

    draw = ImageDraw.Draw(base)
    margin = 20

    # 2) Шрифт
    font_path = "media/fonts/ALS_Story_2.0_R.otf"
    try:
        font = ImageFont.truetype(font_path, 36)
    except Exception:
        logger.warning(f"Не удалось загрузить шрифт {font_path}, используем дефолт")
        font = ImageFont.load_default()

    # 3) Рисуем текст
    draw.text((margin, margin), animal_name, font=font, fill="white")
    line = f"{user_name}, это ты!"
    text_height = font.getsize(line)[1]
    draw.text((margin, base.height - margin - text_height), line, font=font, fill="white")

    # 4) Вставляем логотип
    logo_path = "media/logo/MZoo-logo-circle-black.png"
    if os.path.exists(logo_path):
        try:
            logo = Image.open(logo_path).convert("RGBA")
            logo_width = base.width // 5
            logo = logo.resize(
                (logo_width, int(logo_width * logo.height / logo.width)),
                Image.ANTIALIAS
            )
            pos = (base.width - logo.width - margin, base.height - logo.height - margin)
            base.alpha_composite(logo, dest=pos)
        except Exception:
            logger.exception(f"Не удалось вставить логотип {logo_path}")
    else:
        logger.warning(f"Логотип не найден по пути {logo_path}")

    # 5) Сохраняем итог
    out_dir = "media/generated"
    os.makedirs(out_dir, exist_ok=True)
    filename = f"{user_name}_{animal_name}.png"
    output_path = os.path.join(out_dir, filename)
    base.save(output_path)
    logger.info(f"Сгенерирована картинка результата: {output_path}")

    return output_path
