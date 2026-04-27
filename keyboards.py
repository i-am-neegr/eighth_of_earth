from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

def main_menu() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🎥 Смотреть фильмы"), KeyboardButton(text="🦸 Предложить героя")],
            [KeyboardButton(text="❤️ Поддержать проект"), KeyboardButton(text="📅 Записаться на премьеры")],
            [KeyboardButton(text="🤝 Стать генеральным партнером"), KeyboardButton(text="📰 Новости")],
            [KeyboardButton(text="❓ Задать вопрос проекту")]
        ],
        resize_keyboard=True,
        row_width=2
    )
    return kb


def back_to_menu() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="⬅️ В меню")]],
        resize_keyboard=True
    )


def categories_keyboard(categories, prefix: str = "cat_") -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for cat in categories:
        builder.button(text=cat.name, callback_data=f"{prefix}{cat.id}")
    builder.adjust(1)  # по одной кнопке в ряд
    return builder.as_markup()


def platforms_keyboard(category) -> InlineKeyboardMarkup:
    """Кнопки платформ для вышедшей серии"""
    builder = InlineKeyboardBuilder()
    if category.rutube_url:
        builder.button(text="Rutube", url=category.rutube_url)
    if category.vk_url:
        builder.button(text="VK", url=category.vk_url)
    if category.kion_url:
        builder.button(text="KION", url=category.kion_url)
    if category.okko_url:
        builder.button(text="Okko", url=category.okko_url)
    if category.kinopoisk_url:
        builder.button(text="Кинопоиск", url=category.kinopoisk_url)
    builder.button(text="⬅️ Назад к списку", callback_data="back_to_categories")
    builder.button(text="⬅️ В меню", callback_data="back_to_menu")
    builder.adjust(2)
    return builder.as_markup()


def unreleased_keyboard(category_id) -> InlineKeyboardMarkup:
    """Для серии, которая ещё не вышла"""
    builder = InlineKeyboardBuilder()
    builder.button(text="Смотреть трейлер", url=category.trailer_url)  # category нужно передать
    builder.button(text="Предложить героя для этой серии", callback_data=f"suggest_{category_id}")
    builder.button(text="⬅️ Назад к списку", callback_data="back_to_categories")
    builder.button(text="⬅️ В меню", callback_data="back_to_menu")
    builder.adjust(1)
    return builder.as_markup()