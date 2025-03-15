import asyncpg
from token_key import POSTGRESQL_USER, POSTGRESQL_PASSWORD, \
    POSTGRESQL_DATABASE, POSTGRESQL_HOST


# Данные для подключения к PostgreSQL на локальной машине.
async def get_db_connection():
    return await asyncpg.connect(
        user=POSTGRESQL_USER,
        password=POSTGRESQL_PASSWORD,
        database=POSTGRESQL_DATABASE,
        host=POSTGRESQL_HOST
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
async def get_hotels_and_prices_from_db():
    # Получение соединения с базой данных.
    conn = await get_db_connection()
    try:
        # Выполнение запроса.
        hotels = await conn.fetch('SELECT name, price FROM hotel')
        # Извлечение данных(гостиница и цена) в виде списка.
        return [{'name': hotel['name'], 'price': hotel['price']} for hotel in
                hotels]
    finally:
        # Закрытие соединения.
        await conn.close()


# Функция извлечения названий гостиниц.
async def get_hotels_from_db():
    hotels_and_prices = await get_hotels_and_prices_from_db()
    return [hotel['name'] for hotel in hotels_and_prices]


# Функция извлечения цен гостиниц.
async def get_prices_from_db():
    return await get_hotels_and_prices_from_db()
