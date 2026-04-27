from aiogram import Bot
from sqlalchemy.ext.asyncio import AsyncSession

from models import HeroSuggestion, PremiereSubscriber, PartnerRequest
from config import ADMIN_ID


async def notify_admin_hero(bot: Bot, suggestion: HeroSuggestion):
    """Уведомление админа о новой рекомендации героя"""
    text = (
        f"🦸 <b>Новая рекомендация героя!</b>\n\n"
        f"👤 От пользователя: @{suggestion.username or 'нет username'} "
        f"(ID: <code>{suggestion.user_id}</code>)\n"
        f"📂 Категория: <b>{suggestion.category_id}</b>\n\n"
        f"📝 Описание визионерства:\n{suggestion.description}\n\n"
        f"📞 Контакты:\n{suggestion.contacts}\n\n"
        f"🕒 {suggestion.created_at.strftime('%d.%m.%Y %H:%M')}"
    )

    await bot.send_message(ADMIN_ID, text, parse_mode="HTML")


async def notify_admin_premiere(bot: Bot, subscriber: PremiereSubscriber):
    """Уведомление админа о новой записи на премьеры"""
    text = (
        f"📅 <b>Новая запись на премьеры!</b>\n\n"
        f"👤 Пользователь: @{subscriber.full_name or 'нет имени'} "
        f"(ID: <code>{subscriber.user_id}</code>)\n"
    )

    if subscriber.phone:
        text += f"📱 Телефон: <code>{subscriber.phone}</code>\n"
    if subscriber.email:
        text += f"✉️ Email: {subscriber.email}\n"

    text += f"\n🕒 {subscriber.created_at.strftime('%d.%m.%Y %H:%M')}"

    await bot.send_message(ADMIN_ID, text, parse_mode="HTML")


async def notify_admin_partner(bot: Bot, request: PartnerRequest):
    """Уведомление админа о заявке на генерального партнёра"""
    text = (
        f"🤝 <b>Новая заявка на генерального партнёра!</b>\n\n"
        f"👤 От пользователя: @{request.username or 'нет username'} "
        f"(ID: <code>{request.user_id}</code>)\n\n"
        f"🏢 Информация о компании:\n"
        f"{request.company_info}\n\n"
        f"🕒 {request.created_at.strftime('%d.%m.%Y %H:%M')}"
    )

    await bot.send_message(ADMIN_ID, text, parse_mode="HTML")