import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from user.handlers.handlers import router
from user.handlers.handlers_hotel import router_hotel
from user.antispam import router_antispam
from aiogram.fsm.storage.memory import MemoryStorage
from database.database_postgresql import db_setup
from dotenv import load_dotenv

load_dotenv()


# Запрос на сервер для получения ответа.
async def main():
    # Создание объекта бота и подключение его токена.
    bot = Bot(token=os.getenv('TOKEN'))

    storage = MemoryStorage()  # Использование памяти для хранения состояний.

    # Создание диспетчера для управления ботом.
    dp = Dispatcher(storage=storage)  # Хранение состояния (локальных данных).

    # Инициализация базы данных при старте.
    await db_setup()  # Вызов функции настройки базы данных.

    # Подключение роутера.
    dp.include_router(router)  # Подключение роутера Главного Меню.
    dp.include_router(router_hotel)  # Подключение роутера Гостиница.
    dp.include_router(router_antispam)  # Подключение роутера Антиспам.

    # Игнорирование запросов при выключенном боте.
    await bot.delete_webhook(drop_pending_updates=True)

    await dp.start_polling(bot)


# Запуск бота.
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)  # Подключение логирования.
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Выход')
