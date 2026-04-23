from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery
from .keyboards import main_menu
from .models import Category, HeroSuggestion, PremiereSubscriber, PartnerRequest

router = Router()

class HeroStates(StatesGroup):
    waiting_description = State()
    waiting_contacts = State()

class PartnerStates(StatesGroup):
    waiting_request = State()

@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        "Привет! Добро пожаловать в проект «1/8 Земли: Визионеры России» 🎬\n\n"
        "Здесь вы можете смотреть серии, предлагать героев и поддерживать проект.",
        reply_markup=main_menu()
    )
    # Здесь можно отправить баннер (фото + caption)
    # await message.answer_photo(photo=..., caption=текст_о_проекте)

# === 1. Смотреть фильмы ===
@router.message(F.text == "🎥 Смотреть фильмы")
async def show_categories(message: Message):
    categories = Category.objects.all()
    kb = InlineKeyboardMarkup(inline_keyboard=[])
    for cat in categories:
        kb.inline_keyboard.append([InlineKeyboardButton(text=cat.name, callback_data=f"cat_{cat.id}")])
    await message.answer("Выберите серию:", reply_markup=kb)

@router.callback_query(F.data.startswith("cat_"))
async def show_series(callback: CallbackQuery):
    cat_id = int(callback.data.split("_")[1])
    cat = await Category.objects.get(id=cat_id)  # или .aget в async

    if cat.poster:
        await callback.message.answer_photo(
            photo=cat.poster,
            caption=cat.name + (" — СКОРО" if not cat.is_released else ""),
        )
    else:
        await callback.message.answer(cat.name)

    if cat.is_released:
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Rutube", url=cat.rutube_url)],
            [InlineKeyboardButton(text="VK", url=cat.vk_url)],
            # ... остальные платформы
        ])
    else:
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Смотреть трейлер", url=cat.trailer_url)],
            [InlineKeyboardButton(text="Предложить героя для этой серии", callback_data=f"suggest_{cat.id}")]
        ])

    await callback.message.answer("Выберите платформу или действие:", reply_markup=kb)
    await callback.answer()

# === 2. Предложить героя ===
@router.message(F.text == "🦸 Предложить героя")
async def suggest_hero_start(message: Message, state: FSMContext):
    # Показываем только актуальные категории (технологии, спорт и т.д.)
    await message.answer(
        "Для каких серий вы хотите предложить героя?\n"
        "Кто нам подходит: ... (текст от Ульяны)\n\n"
        "Опишите героя и его визионерство:",
        reply_markup=...  # клавиатура с категориями
    )
    await state.set_state(HeroStates.waiting_description)

@router.message(HeroStates.waiting_description)
async def hero_description(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    await message.answer("Теперь укажите контакты героя (телефон, telegram, почта и т.д.):")
    await state.set_state(HeroStates.waiting_contacts)

@router.message(HeroStates.waiting_contacts)
async def hero_contacts(message: Message, state: FSMContext):
    data = await state.get_data()
    suggestion = HeroSuggestion.objects.create(
        user_id=message.from_user.id,
        username=message.from_user.username,
        category_id=...,  # нужно сохранить категорию раньше
        description=data['description'],
        contacts=message.text
    )
    # Отправка вам в Telegram или на почту (через asyncio)
    await message.answer("Спасибо! Мы получили вашу рекомендацию 🙌", reply_markup=main_menu())
    await state.clear()

# Аналогично реализуй остальные пункты: Поддержать, Премьеры, Партнёрство, Новости, Задать вопрос.

# Для "Записаться на премьеры" — можно использовать ReplyKeyboard с кнопкой "Отправить контакт"
# или RequestContact.