import asyncio
from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.enums import ParseMode
import user.keyboards as kb

router = Router()  # Создание объекта.

# Текст приветствия.
text_welcome = (
    "<b>Добро пожаловать в наш мир комфорта и удобства!</b>\n"
    "Мы рады приветствовать вас на нашей платформе для бронирования мест! "
    "Здесь вы сможете легко и быстро найти идеальное пространство для вашего "
    "мероприятия, отдыха или деловых встреч.\n\n"
    "<b>Почему выбирают нас?</b>\n\n"
    "<b>•	Широкий выбор:</b> У нас представлены разнообразные локации — от "
    "уютных кафе до современных конференц-залов.\n"
    "<b>•	Удобный интерфейс:</b> Бронирование стало проще, чем когда-либо. "
    "Всего несколько кликов, и ваше место забронировано!\n"
    "<b>•	Гарантия качества:</b> Мы тщательно подберем каждую локацию, "
    "чтобы вы могли быть уверены в высоком уровне сервиса.\n\n"
    "<b>Начните ваш отдых с нами уже сегодня!</b>\n\n"
    "Если у вас возникли вопросы или нужна помощь, наша команда всегда готова "
    "помочь!"
)


# Перехват на запрос '/start'.
@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        text='Вас приветствует чат-бот <b><u>системы бронирования '
             'площадки.</u></b>',  # Ответ пользователю.
        parse_mode=ParseMode.HTML,  # Форматирование текста(выделение и
        # подчеркивание).
        reply_markup=kb.inline_details  # Подключение Inline-клавиатуры.
    )


# Обработка нажатия Inline-кнопки через CallBack.
@router.callback_query(F.data == 'details')
async def cm_start(callback: CallbackQuery):
    await callback.answer('')  # Чтоб не 'светилась' кнопка после нажатия.
    await callback.message.answer(
        text=text_welcome,
        parse_mode=ParseMode.HTML,

        # Подключение Inline-клавиатуры для просмотра предлагаемых площадок.
        reply_markup=kb.inline_list_places
    )


# Обработка Inline-клавиатуры для просмотра предлагаемых площадок.
@router.callback_query(F.data.startswith('place_'))
async def get_callback_query_places(callback: CallbackQuery):
    if callback.data in [
        'place_cafe', 'place_restaurant', 'place_hotel',
        'place_SPA', 'place_country_house', 'place_other_places'
    ]:
        if callback.data == 'place_cafe':
            await callback.answer(text='Временно недоступно')
        elif callback.data == 'place_restaurant':
            await callback.answer(text='Временно недоступно')
        elif callback.data == 'place_hotel':
            await callback.answer(text='Временно недоступно')
        elif callback.data == 'place_SPA':
            await callback.answer(text='Временно недоступно')
        elif callback.data == 'place_country_house':
            await callback.answer(text='Временно недоступно')
        elif callback.data == 'place_other_places':
            await callback.answer(text='Временно недоступно')
