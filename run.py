import asyncio
import logging

from aiogram import Bot, Dispatcher
from token_key import TOKEN
from user.handlers import router


# Запрос на сервер для получения ответа.
async def main():
    bot = Bot(token=TOKEN)  # Создание объекта бота и подключение его токена.
    dp = Dispatcher()  # Создание диспетчера для управления ботом.
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