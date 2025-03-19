from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from database.database_postgresql import get_hotels_from_db


# Создание клавиатуры через сборщик InlineKeyboardBuilder для раздела
# "Гостиница" из списка в базе данных и добавление кнопок пагинации.
async def build_button_places_hotel(page: int = 0, items_per_page: int = 15):
    # Получаем названия гостиниц из базы данных.
    hotels = await get_hotels_from_db()

    # Разделяем список гостиниц на страницы.
    start = page * items_per_page
    end = start + items_per_page
    hotels_page = hotels[start:end]

    # Вычисляем общее количество страниц.
    total_pages = (len(hotels) + items_per_page - 1) // items_per_page

    keyboard = InlineKeyboardBuilder()

    for hotel in hotels_page:
        keyboard.add(
            InlineKeyboardButton(text=hotel, callback_data=f'hotel_{hotel}')
        )

    keyboard.adjust(3)  # Количество кнопок в ряд.

    # Добавляем кнопки пагинации, если это необходимо.
    if page > 0:
        keyboard.row(InlineKeyboardButton(text='⬅️ Назад',
                                          callback_data=f'page_{page - 1}'))
    if end < len(hotels):
        keyboard.row(InlineKeyboardButton(text='Вперед ➡️',
                                          callback_data=f'page_{page + 1}'))

    # Добавляем кнопку индикатора страницы, если это необходимо.
    if len(hotels) > items_per_page:
        keyboard.row(
            InlineKeyboardButton(text=f'Страница {page + 1} из {total_pages}',
                                 callback_data='page_indicator'))

    # Добавление кнопку "В главное меню" под всеми остальными кнопками.
    keyboard.row(
        InlineKeyboardButton(text='В главное меню ⤴️',
                             callback_data='main_menu'))

    return keyboard.as_markup()


# Создание кнопок под выбранной Гостиницей.
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

    # Добавляем кнопку "Назад" под всеми остальными кнопками.
    keyboard_joint.row(
        InlineKeyboardButton(text='⬅️ Назад', callback_data='back_hotel_main'))

    return keyboard_joint.as_markup()


# Создание кнопки "Назад" под описанием выбранной Гостиницы.
def get_back_button():
    back_button = InlineKeyboardButton(
        text='⬅️ Назад',
        callback_data='back_hotel_details')
    return InlineKeyboardMarkup(inline_keyboard=[[back_button]])
