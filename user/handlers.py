import asyncio
from aiogram import Router, F
from aiogram.filters import CommandStart, StateFilter
from aiogram.types import Message, CallbackQuery
from aiogram.enums import ParseMode
import user.keyboards as kb
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

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


# Объявление состояния бота.
class Form(StatesGroup):
    waiting_for_details = State()


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
async def cm_start(callback: CallbackQuery, state: FSMContext):
    # Замена текста приветствия.
    await callback.message.edit_text(
        text=text_welcome,
        parse_mode=ParseMode.HTML,

        # Подключение Inline-клавиатуры для просмотра предлагаемых площадок.
        reply_markup=kb.inline_list_places
    )
    await state.set_state(Form.waiting_for_details)  # Устанавливаем состояние.


# Обработка Inline-клавиатуры для просмотра предлагаемых площадок.
@router.callback_query(F.data.startswith('place_'),
                       StateFilter(Form.waiting_for_details))
async def get_callback_query_places(callback: CallbackQuery,
                                    state: FSMContext):
    # Список предлагаемых площадок.
    if callback.data in [
        'place_cafe', 'place_restaurant', 'place_hotel',
        'place_SPA', 'place_country_house', 'place_other_places'
    ]:
        if callback.data == 'place_cafe':
            await callback.answer(text='Временно недоступно')

        elif callback.data == 'place_restaurant':
            await callback.answer(text='Временно недоступно')

        # Переход в раздел Гостиница.
        elif callback.data == 'place_hotel':
            # Установка состояния для раздела.
            await state.set_state(Form.waiting_for_details)
            await callback.message.edit_text(
                text='Вы выбрали раздел <b><u>Гостиница</u></b>',
                # Подключение Inline-клавиатуры со списком гостиниц.
                parse_mode=ParseMode.HTML,
                reply_markup=await kb.build_button_places_hotel()
            )

        elif callback.data == 'place_SPA':
            await callback.answer(text='Временно недоступно')

        elif callback.data == 'place_country_house':
            await callback.answer(text='Временно недоступно')

        elif callback.data == 'place_other_places':
            await callback.answer(text='Временно недоступно')


# Обработка при нажатии кн.'Назад'.
@router.callback_query(F.data == 'back')
async def handle_back_button(callback: CallbackQuery, state: FSMContext):
    await callback.answer()  # Очищаем уведомление.
    # Возврат в состояние выбора мест.
    await state.set_state(Form.waiting_for_details)
    await callback.message.edit_text(
        text='Вы вернулись в меню выбора мест',
        reply_markup=kb.inline_list_places
    )


# Временное уведомление при нажатии кнопок выбора гостиниц.
@router.callback_query(F.data)
async def handle_button(callback_query: CallbackQuery):
    await callback_query.answer(f'Вы выбрали: {callback_query.data}')
