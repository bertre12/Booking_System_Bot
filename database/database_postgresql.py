import asyncpg
import os
from dotenv import load_dotenv

load_dotenv()


# Данные для подключения к PostgreSQL на локальной машине.
async def get_db_connection():
    return await asyncpg.connect(
        user=os.getenv("POSTGRESQL_USER"),
        password=os.getenv("POSTGRESQL_PASSWORD"),
        database=os.getenv("POSTGRESQL_DATABASE"),
        host=os.getenv("POSTGRESQL_HOST"),
    )


# Функция создания таблиц в базе данных.
async def db_setup():
    # Получение соединения с базой данных.
    conn = await get_db_connection()
    try:
        # Создание таблицы hotel.
        await conn.execute(
            """
            CREATE TABLE IF NOT EXISTS hotel (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                price DOUBLE PRECISION NOT NULL,
                description TEXT
            )
        """
        )

        # Создание таблицы users и связи 'один ко многим'.
        await conn.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                phone_number VARCHAR(20) NOT NULL,
                email TEXT,
                hotel_id INTEGER NOT NULL,
                booking_number TEXT NOT NULL,
                FOREIGN KEY (hotel_id) REFERENCES hotel(id) ON DELETE CASCADE
            )
        """
        )
        print('База данных PostgreSQL подключена и таблицы созданы.')
    finally:
        # Закрытие соединения.
        try:
            await conn.close()
        except Exception as e:
            print(f'Ошибка при закрытии соединения: {e}')


# Функция для запроса к базе данных.
async def get_id_hotel_and_price_and_description_from_db():
    # Получение соединения с базой данных.
    conn = await get_db_connection()
    try:
        # Выполнение запроса.
        hotels = await conn.fetch("SELECT id, name, price, description FROM " 
                                  "hotel")
        # Извлечение данных(id, гостиница, цена, описание) в виде списка.
        return [
            {
                "id": hotel["id"],
                "name": hotel["name"],
                "price": hotel["price"],
                "description": hotel["description"],
            }
            for hotel in hotels
        ]
    finally:
        # Закрытие соединения.
        await conn.close()


# Функция извлечения id названия гостиницы.
async def get_hotel_id_from_db(hotel_name: str):
    conn = await get_db_connection()
    result = await conn.fetchrow("SELECT id FROM hotel WHERE name = $1",
                                 hotel_name)
    await conn.close()
    return result["id"] if result else None


# Функция извлечения названий гостиниц.
async def get_hotels_from_db():
    # Получаем данные из бд.
    hotels_and_prices = await get_id_hotel_and_price_and_description_from_db()

    # Извлекаем названия гостиниц и сортируем их по алфавиту.
    hotels = [hotel["name"] for hotel in hotels_and_prices]
    hotels.sort()  # Сортировка по алфавиту.

    return hotels


# Функция извлечения цены для выбранной гостиницы.
async def get_prices_from_db():
    return await get_id_hotel_and_price_and_description_from_db()


# Функция извлечения описания для выбранной гостиницы.
async def get_descriptions_from_db():
    # Получаем данные из бд.
    hotels_and_descriptions = \
        await get_id_hotel_and_price_and_description_from_db()
    return [hotel["description"] for hotel in hotels_and_descriptions]


# Функция для записи данных в таблицу users.
async def save_user(user_data):
    # Получаем соединение с базой данных.
    conn = await get_db_connection()
    try:
        await conn.execute(
            """INSERT INTO users (
            name, phone_number, email, hotel_id, booking_number
            )
            VALUES ($1, $2, $3, $4, $5)
        """,
            user_data["name"],
            user_data["phone_number"],
            user_data["email"],
            user_data["hotel_id"],
            user_data["booking_number"],
        )
        print('Данные успешно добавлены в таблицу users.')
    except Exception as e:
        print(f'Ошибка при добавлении данных: {e}')
    finally:
        # Закрываем соединение.
        try:
            await conn.close()
        except Exception as e:
            print(f'Ошибка при закрытии соединения: {e}')
