from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, Contact
from sqlalchemy import insert
from database import async_session
from models import PremiereSubscriber
from keyboards import back_to_menu, main_menu
from utils import notify_admin_premiere

router = Router()

@router.message(F.text == "📅 Записаться на премьеры")
async def premiere_subscription(message: Message):
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📱 Отправить мой контакт", request_contact=True)],
            [KeyboardButton(text="⬅️ В меню")]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )

    await message.answer(
        "Оставьте контакт, чтобы мы могли пригласить вас на премьеры и показы новых серий 🎟️\n\n"
        "Нажимайте кнопку ниже или введите данные вручную (ФИО + телефон / почта).",
        reply_markup=kb
    )


@router.message(F.contact)
async def handle_contact(message: Message):
    contact = message.contact
    async with async_session() as session:
        sub = PremiereSubscriber(
            user_id=message.from_user.id,
            full_name=contact.full_name,
            phone=contact.phone_number
        )
        session.add(sub)
        await session.commit()

    await notify_admin_premiere(message.bot, sub)  # реализуй в utils.py
    await message.answer(
        "✅ Готово! Мы сообщим вам о ближайших показах 🎬",
        reply_markup=back_to_menu()
    )


@router.message(F.text == "⬅️ В меню")  # можно вынести в общий хендлер
async def back_menu(message: Message):
    await message.answer("Главное меню", reply_markup=main_menu())