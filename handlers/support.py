from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from keyboards import back_to_menu

router = Router()

@router.message(F.text == "❤️ Поддержать проект")
async def support_project(message: Message):
    await message.answer(
        "Вы можете поддержать проект по ссылке ниже 👇",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Поддержать", url="https://netmonet.ru/твоя_ссылка")]
        ])
    )
    await message.answer("⬅️ В меню", reply_markup=back_to_menu())