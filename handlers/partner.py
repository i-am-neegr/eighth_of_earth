from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, FSInputFile, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from database import async_session
from models import PartnerRequest
from states import PartnerForm
from keyboards import back_to_menu
from utils import notify_admin_partner

router = Router()

@router.message(F.text == "🤝 Стать генеральным партнером")
async def become_partner(message: Message):
    text = (
        "Герой компании включён в сценарий серии\n\n"
        "• Логотип и статус «Генеральный партнёр серии»\n"
        "• Закрытый показ серии для сообщества компании\n"
        "• 5 билетов на закрытую премьеру с топ-менеджерами, СМИ и VIP-гостями"
    )

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📩 Оставить заявку", callback_data="partner_request")],
        [InlineKeyboardButton(text="📄 Получить презентацию", callback_data="partner_presentation")]
    ])

    await message.answer(text, reply_markup=kb)


@router.callback_query(F.data == "partner_request")
async def partner_request(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text("Оставьте контакт и коротко опишите вашу компанию:")
    await state.set_state(PartnerForm.waiting_info)
    await callback.answer()


@router.message(PartnerForm.waiting_info)
async def save_partner_request(message: Message, state: FSMContext):
    async with async_session() as session:
        req = PartnerRequest(
            user_id=message.from_user.id,
            username=message.from_user.username,  # ← добавили
            company_info=message.text
        )
        session.add(req)
        await session.commit()

    await notify_admin_partner(message.bot, req)
    await message.answer("✅ Заявка отправлена! Мы свяжемся с вами.", reply_markup=back_to_menu())
    await state.clear()


@router.callback_query(F.data == "partner_presentation")
async def send_presentation(callback: CallbackQuery):
    doc = FSInputFile("media/presentation.pdf")   # положи файл в папку media
    await callback.message.answer_document(doc, caption="Презентация для генеральных партнёров")
    await callback.answer()