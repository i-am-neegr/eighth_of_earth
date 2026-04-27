from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from sqlalchemy import select
from database import async_session
from models import Category, HeroSuggestion
from states import HeroForm
from keyboards import categories_keyboard, back_to_menu
from utils import notify_admin_hero

router = Router()

@router.message(F.text == "🦸 Предложить героя")
async def suggest_hero(message: Message, state: FSMContext):
    async with async_session() as session:
        # Только актуальные категории для предложений
        result = await session.execute(
            select(Category).where(Category.name.in_(["Технологии", "Спорт", "Природа и экология", "Культура и искусство"]))
        )
        categories = result.scalars().all()

    await message.answer(
        "Для каких серий вы хотите предложить героя?\n\n"
        "<b>Кто нам подходит:</b> текст от Ульяны...\n"
        "Дедлайн: 23-24 апреля!\n\n"
        "Выберите категорию:",
        reply_markup=categories_keyboard(categories, prefix="suggest_")
    )
    await state.set_state(HeroForm.waiting_category)


@router.callback_query(F.data.startswith("suggest_"), HeroForm.waiting_category)
async def hero_category_chosen(callback: CallbackQuery, state: FSMContext):
    cat_id = int(callback.data.split("_")[1])
    await state.update_data(category_id=cat_id)

    await callback.message.edit_text(
        "Опишите героя и его визионерство (свободная форма):"
    )
    await state.set_state(HeroForm.waiting_description)
    await callback.answer()


@router.message(HeroForm.waiting_description)
async def hero_description(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    await message.answer("Теперь укажите контакты героя (Telegram, телефон, почта и любая доп. информация):")
    await state.set_state(HeroForm.waiting_contacts)


@router.message(HeroForm.waiting_contacts)
async def hero_contacts(message: Message, state: FSMContext):
    data = await state.get_data()
    async with async_session() as session:
        suggestion = HeroSuggestion(
            user_id=message.from_user.id,
            username=message.from_user.username,
            category_id=data['category_id'],
            description=data['description'],
            contacts=message.text
        )
        session.add(suggestion)
        await session.commit()

    # Отправляем уведомление админу
    await notify_admin_hero(message.bot, suggestion)

    await message.answer(
        "✅ Спасибо! Мы получили вашу рекомендацию 🙌",
        reply_markup=back_to_menu()
    )
    await state.clear()