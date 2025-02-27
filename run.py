import asyncio
import logging

from aiogram import Bot, Dispatcher
from token_key import TOKEN
from user.handlers import router
from aiogram.fsm.storage.memory import MemoryStorage


# Запрос на сервер для получения ответа.
async def main():
    bot = Bot(token=TOKEN)  # Создание объекта бота и подключение его токена.
    storage = MemoryStorage()  # Использование памяти для хранения состояний.
    dp = Dispatcher(storage=storage)  # Создание диспетчера для управления
    # ботом + сохранение состояния(локальных данных).
    dp.include_router(router)  # Подключение роутера.
    await bot.delete_webhook(drop_pending_updates=True)  # Игнорирование
    # запросов при выключенном боте.
    await dp.start_polling(bot)


# Запуск бота.
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)  # Подключение логирования.
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Выход')