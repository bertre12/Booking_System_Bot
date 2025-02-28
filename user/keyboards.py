from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

# Создание Inline-клавиатуры.
inline_details = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Подробнее', callback_data='details')
         ]
    ]
)
# Создание Inline-клавиатуры для просмотра списка площадок отдыха.
inline_list_places = InlineKeyboardMarkup(
    inline_keyboard=[
        # Кнопки 1-го ряда.
        [InlineKeyboardButton(text='Кафе',
                              callback_data='place_cafe'),
         InlineKeyboardButton(text='Ресторан',
                              callback_data='place_restaurant'),
         InlineKeyboardButton(text='Гостиница',
                              callback_data='place_hotel')],
        # Кнопки 2-го ряда.
        [InlineKeyboardButton(text='СПА-салон',
                              callback_data='place_SPA'),
         InlineKeyboardButton(text='Усадьба',
                              callback_data='place_country_house'),
         InlineKeyboardButton(text='Другие места',
                              callback_data='place_other_places')
         ]
    ]
)


# Создание клавиатуры через сборщик InlineKeyboardBuilder.
async def build_button_places_hotel():
    # Список доступных гостиниц.
    data = (
        'Willing', 'Полонез', 'Imperial Palace', 'БонОтель', 'Buta',
        'Crowne Plaza Minsk', 'Турист', 'Беларусь', 'Орбита', 'IT Time',
        'Славянская', 'Гостиница')

    keyboard = InlineKeyboardBuilder()

    for button in data:
        keyboard.add(InlineKeyboardButton(text=button, callback_data=button))

    keyboard.adjust(3)  # Количество кнопок в ряд.

    # Добавление кнопку "Назад" под всеми остальными кнопками.
    keyboard.row(InlineKeyboardButton(text='Назад', callback_data='back'))

    return keyboard.as_markup()
