import asyncio
import logging

from aiogram import Bot, Dispatcher
from token_key import TOKEN
from user.handlers.handlers import router
from user.handlers.handlers_hotel import router_hotel
from aiogram.fsm.storage.memory import MemoryStorage
from database.database_postgresql import db_setup


# Запрос на сервер для получения ответа.
async def main():
    bot = Bot(token=TOKEN)  # Создание объекта бота и подключение его токена.
    storage = MemoryStorage()  # Использование памяти для хранения состояний.
    dp = Dispatcher(storage=storage)  # Создание диспетчера для управления
    # ботом + сохранение состояния(локальных данных).

    # Инициализация базы данных при старте.
    await db_setup()  # Вызов функции настройки базы данных.

    dp.include_router(router)  # Подключение роутера.
    dp.include_router(router_hotel)  # Подключение роутера.

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
