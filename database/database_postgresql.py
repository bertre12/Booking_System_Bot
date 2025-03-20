import asyncpg
import os
from dotenv import load_dotenv

load_dotenv()


# Данные для подключения к PostgreSQL на локальной машине.
async def get_db_connection():
    return await asyncpg.connect(
        user=os.getenv('POSTGRESQL_USER'),
        password=os.getenv('POSTGRESQL_PASSWORD'),
        database=os.getenv('POSTGRESQL_DATABASE'),
        host=os.getenv('POSTGRESQL_HOST')
    )


# Функция создания таблиц в базе данных.
async def db_setup():
    # Получение соединения с базой данных.
    conn = await get_db_connection()
    try:
        # Создание таблицы hotel.
        await conn.execute('''
            CREATE TABLE IF NOT EXISTS hotel (
                id SERIAL PRIMARY KEY,
                name TEXT,
                price INTEGER,
                description TEXT
            )
        ''')
        print('База данных PostgreSQL подключена и таблицы созданы.')
    finally:
        # Закрытие соединения.
        await conn.close()


# Функция для запроса к базе данных.
async def get_hotels_and_prices_and_description_from_db():
    # Получение соединения с базой данных.
    conn = await get_db_connection()
    try:
        # Выполнение запроса.
        hotels = await conn.fetch('SELECT name, price, description FROM hotel')
        # Извлечение данных(гостиница и цена, описание) в виде списка.
        return [{'name': hotel['name'], 'price': hotel['price'],
                 'description': hotel['description']} for hotel in
                hotels]
    finally:
        # Закрытие соединения.
        await conn.close()


# Функция извлечения названий гостиниц.
async def get_hotels_from_db():
    # Получаем данные из бд.
    hotels_and_prices = await get_hotels_and_prices_and_description_from_db()

    # Извлекаем названия гостиниц и сортируем их по алфавиту.
    hotels = [hotel['name'] for hotel in hotels_and_prices]
    hotels.sort()  # Сортировка по алфавиту.

    return hotels


# Функция извлечения цены для выбранной гостиницы.
async def get_prices_from_db():
    return await get_hotels_and_prices_and_description_from_db()


# Функция извлечения описания для выбранной гостиницы.
async def get_descriptions_from_db():
    # Получаем данные из бд.
    hotels_and_descriptions = \
        await get_hotels_and_prices_and_description_from_db()
    return [hotel['description'] for hotel in hotels_and_descriptions]
