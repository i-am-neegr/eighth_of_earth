from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, FSInputFile
from sqlalchemy import select
from database import async_session
from models import Category
from keyboards import categories_keyboard, platforms_keyboard, unreleased_keyboard, back_to_menu, main_menu

router = Router()

@router.message(F.text == "🎥 Смотреть фильмы")
async def show_films(message: Message):
    async with async_session() as session:
        result = await session.execute(select(Category))
        categories = result.scalars().all()

    if not categories:
        await message.answer("Пока нет серий 😔")
        return

    await message.answer(
        "Выберите отрасль / серию:",
        reply_markup=categories_keyboard(categories)
    )


@router.callback_query(F.data.startswith("cat_"))
async def show_category(callback: CallbackQuery):
    cat_id = int(callback.data.split("_")[1])

    async with async_session() as session:
        category = await session.get(Category, cat_id)

    if not category:
        await callback.answer("Серия не найдена")
        return

    # Отправляем постер, если есть
    if category.poster_path:
        photo = FSInputFile(category.poster_path)
        await callback.message.answer_photo(
            photo=photo,
            caption=f"<b>{category.name}</b>" + (" — СКОРО" if not category.is_released else "")
        )
    else:
        await callback.message.answer(
            f"<b>{category.name}</b>" + (" — СКОРО" if not category.is_released else "")
        )

    # Кнопки в зависимости от статуса
    if category.is_released:
        kb = platforms_keyboard(category)
    else:
        kb = unreleased_keyboard(category.id)   # нужно доработать под trailer_url

    await callback.message.answer("Выберите действие:", reply_markup=kb)
    await callback.answer()


@router.callback_query(F.data == "back_to_categories")
async def back_to_categories(callback: CallbackQuery):
    # Повторяем логику show_films
    async with async_session() as session:
        result = await session.execute(select(Category))
        categories = result.scalars().all()

    await callback.message.edit_text("Выберите отрасль / серию:", reply_markup=categories_keyboard(categories))
    await callback.answer()


@router.callback_query(F.data == "back_to_menu")
async def back_to_main_menu(callback: CallbackQuery):
    await callback.message.answer("Главное меню:", reply_markup=main_menu())  # или edit_text
    await callback.answer()