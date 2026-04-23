from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

def main_menu():
    kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    kb.add(
        KeyboardButton("🎥 Смотреть фильмы"),
        KeyboardButton("🦸 Предложить героя"),
        KeyboardButton("❤️ Поддержать проект"),
    )
    kb.add(
        KeyboardButton("📅 Записаться на премьеры"),
        KeyboardButton("🤝 Стать генеральным партнером"),
    )
    kb.add(KeyboardButton("📰 Новости"), KeyboardButton("❓ Задать вопрос проекту"))
    return kb

# и т.д. для других меню (список категорий, платформы и т.п.)