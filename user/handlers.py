import asyncio
from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.enums import ParseMode

router = Router()  # Создание объекта.


# Перехват на запрос '/start'.
@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        text='Вас приветствует чат-бот <b><u>системы бронирования '
             'площадки.</u></b>',  # Ответ пользователю.
        parse_mode=ParseMode.HTML  # Форматирование текста(выделение и
        # подчеркивание).
    )
