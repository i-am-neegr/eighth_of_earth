# bot/management/commands/runbot.py
from django.core.management.base import BaseCommand
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from bot.handlers import router
import asyncio
from django.conf import settings

class Command(BaseCommand):
    help = 'Запуск Telegram бота'

    def handle(self, *args, **options):
        bot = Bot(token=settings.TELEGRAM_BOT_TOKEN, default=DefaultBotProperties(parse_mode='HTML'))
        dp = Dispatcher()
        dp.include_router(router)
        asyncio.run(dp.start_polling(bot))