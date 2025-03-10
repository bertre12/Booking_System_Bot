from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from database.database_postgresql import get_hotels_from_db


# Создание клавиатуры через сборщик InlineKeyboardBuilder для раздела
# 'Гостиница' из списка в базе данных.
async def build_button_places_hotel():
    # Получаем названия гостиниц из базы данных.
    hotels = await get_hotels_from_db()

    keyboard = InlineKeyboardBuilder()

    for hotel in hotels:
        keyboard.add(InlineKeyboardButton(text=hotel, callback_data=hotel))

    keyboard.adjust(3)  # Количество кнопок в ряд.

    # Добавление кнопку "В главное меню" под всеми остальными кнопками.
    keyboard.row(InlineKeyboardButton(text='В главное меню',
                                      callback_data='main_menu'))

    return keyboard.as_markup()


async def build_button_places_hotel_joint():
    # Список кнопок.
    data = (
        'Подробнее', 'Цена', 'Свободные даты', 'Забронировать'
    )

    keyboard_joint = InlineKeyboardBuilder()

    for button in data:
        keyboard_joint.add(
            InlineKeyboardButton(text=button, callback_data=button))

    keyboard_joint.adjust(2)  # Количество кнопок в ряд.

    # Добавление кнопку "Назад" под всеми остальными кнопками.
    keyboard_joint.row(InlineKeyboardButton(text='Назад',
                                            callback_data='back_hotel'))

    return keyboard_joint.as_markup()
