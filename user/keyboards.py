from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Создание Inline-клавиатуры.
inline = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Подробнее', callback_data='details')
         ]
    ]
)
