from aiogram import Router
from aiogram.types import Message
import asyncio

router_antispam = Router()


# Удаление сообщений от пользователя(простой анти спам).
@router_antispam.message()
async def delete_message(message: Message):
    # Отправка подтверждения о получении сообщения и предупреждение.
    bot_message = await message.answer(
        'Ваше сообщение получено!\nИ будет удалено через 3 секунд'
    )

    # Удаление сообщений пользователя через 5 секунд.
    await asyncio.sleep(3)
    await message.delete()
    # Удаление сообщения от бота.
    await bot_message.delete()