from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, FSInputFile
from keyboards import main_menu

router = Router()

@router.message(Command("start"))
async def cmd_start(message: Message):
    # Можно отправить баннер (замени путь на свой)
    # photo = FSInputFile("media/banner.jpg")
    # await message.answer_photo(
    #     photo=photo,
    #     caption="Приветствие + текст о проекте «1/8 Земли: Визионеры России»\n\n"
    #             "Мы рассказываем истории людей, которые меняют отрасли.",
    #     reply_markup=main_menu()
    # )

    await message.answer(
        "👋 Привет! Добро пожаловать в проект <b>1/8 Земли: Визионеры России</b> 🎬\n\n"
        "Здесь ты можешь смотреть вдохновляющие серии, предлагать героев и поддерживать проект.",
        reply_markup=main_menu()
    )