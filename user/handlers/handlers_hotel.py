from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
import user.keyboards.keyboards as kb
import user.keyboards.keyboards_hotel as kb_hotel
from database.database_postgresql import get_prices_from_db, \
    get_hotels_and_prices_and_description_from_db
from user.handlers.handlers import Form

router_hotel = Router()  # Создание объекта.


# Обработка кнопок выбора названий Гостиниц и добавление пагинации.
@router_hotel.callback_query(F.data.startswith('hotel_'))
async def get_callback_query_hotel_it_time(callback: CallbackQuery,
                                           state: FSMContext):
    # Извлекаем название гостиницы.
    hotel_name = callback.data.split('_')[1]

    # Сохраняем название гостиницы в состоянии.
    await state.update_data(hotel_name=hotel_name)

    # Устанавливаем состояние.
    await state.set_state(Form.waiting_for_hotel_details)

    # Отправляем сообщение с выбранным названием гостиницы.
    await callback.message.edit_text(
        text=f'Вы выбрали отель <b><u>{hotel_name}</u></b>',
        parse_mode=ParseMode.HTML,
        reply_markup=await kb_hotel.build_button_places_hotel_joint()
    )


# Обработка пагинации при выборе Гостиница.
@router_hotel.callback_query(lambda c: c.data.startswith('page_'))
async def handle_pagination(callback: CallbackQuery):
    # Извлекаем данные из callback.
    data = callback.data.split('_')

    # Проверяем, является ли callback-данные кнопкой пагинации.
    if len(data) == 2 and data[1].isdigit():
        page = int(data[1])  # Преобразуем номер страницы в число.
        # Обновляем клавиатуру с новой страницей.
        keyboard = await kb_hotel.build_button_places_hotel(page=page)
        await callback.message.edit_reply_markup(reply_markup=keyboard)
    else:
        # Игнорируем нажатие на кнопку индикатора страницы.
        await callback.answer()

    # Подтверждаем обработку callback.
    await callback.answer()


# Обработка кнопки для перехода в главное меню.
@router_hotel.callback_query(F.data == 'main_menu')
async def handle_back_button(callback: CallbackQuery, state: FSMContext):
    await callback.answer()  # Очищаем уведомление.
    # Возврат в состояние выбора мест.
    await state.set_state(Form.waiting_for_details)

    await callback.message.edit_text(
        text='Вы перешли в раздел <b><u>раздел выбора мест отдыха:</u></b>',
        parse_mode=ParseMode.HTML,

        # Подключаем Inline-клавиатуру со списком площадок отдыха.
        reply_markup=kb.inline_list_places
    )


# Обработка при нажатии кн."Назад" переход в меню Гостиница.
@router_hotel.callback_query(F.data == 'back_hotel_main')
async def handle_back_button_main(callback: CallbackQuery, state: FSMContext):
    await callback.answer()  # Очищаем уведомление.

    # Возврат в состояние выбора Гостиница.
    await state.set_state(Form.waiting_for_hotel_details)

    await callback.message.edit_text(
        text='Вы выбрали раздел <b><u>Гостиница</u></b>',
        parse_mode=ParseMode.HTML,

        # Подключаем Inline-клавиатуру со списком гостиниц.
        reply_markup=await kb_hotel.build_button_places_hotel()
    )


# Обработка при нажатии кн. "Подробнее".
@router_hotel.callback_query(F.data == 'Подробнее')
async def handle_more_details(callback: CallbackQuery, state: FSMContext):
    # Извлекаем название гостиницы из состояния.
    data = await state.get_data()
    hotel_name = data.get('hotel_name', 'неизвестный отель')

    # Получаем данные о гостинице через подключение к бд.
    hotels_and_prices = await get_hotels_and_prices_and_description_from_db()
    hotel_description = next(
        (hotel['description'] for hotel in hotels_and_prices if
         hotel['name'] == hotel_name), None)

    # Обрабатываем ошибку, когда нет информации о выбранной гостинице.
    if not hotel_description:
        await callback.answer(
            text='Ошибка: Описание для гостиницы не найдено или недоступно.',
            show_alert=True  # Всплывающее сообщение.
        )
        return

    await callback.message.edit_text(
        text=f'Описание отеля <b><u>{hotel_name}</u></b>: {hotel_description}',
        parse_mode=ParseMode.HTML,

        # Подключаем кнопку "Назад".
        reply_markup=kb_hotel.get_back_button()
    )
    # Подтверждаем обработку callback-запроса.
    await callback.answer()


@router_hotel.callback_query(F.data == 'Цена')
async def handle_price(callback: CallbackQuery, state: FSMContext):
    # Извлекаем название гостиницы из состояния.
    data = await state.get_data()
    hotel_name = data.get('hotel_name', 'неизвестный отель')

    # Получаем цены из базы данных.
    prices = await get_prices_from_db()

    # Находим цену для выбранной гостиницы.
    hotel_price = next(
        (price['price'] for price in prices if price['name'] == hotel_name),
        None)

    # Обрабатываем ошибку.
    if not hotel_price:
        await callback.answer(text='Ошибка: Цена для отеля не найдена.',
                              show_alert=True)
        return

    # Отправляем сообщение с информацией о цене.
    await callback.message.edit_text(
        text=f'Цена в отеле <b><u>{hotel_name}</u></b>: <b>{hotel_price}</b> '
             f'руб.',
        parse_mode=ParseMode.HTML,

        # Подключаем кнопку "Назад".
        reply_markup=kb_hotel.get_back_button()
    )
    # Подтверждаем обработку callback-запроса.
    await callback.answer()


# Обработка при нажатии кн."Назад".
@router_hotel.callback_query(F.data == 'back_hotel_details')
async def handle_back_button_details(callback: CallbackQuery,
                                     state: FSMContext):
    await callback.answer()  # Очищаем уведомление.

    # Извлекаем название гостиницы из состояния.
    data = await state.get_data()
    hotel_name = data.get('hotel_name', 'неизвестный отель')

    # Возврат к предыдущему сообщению.
    await callback.message.edit_text(
        text=f'Вы вернулись к выбранному отелю <b><u>{hotel_name}</u></b>',
        parse_mode=ParseMode.HTML,

        # Подключаем кнопки под выбранной Гостиницей.
        reply_markup=await kb_hotel.build_button_places_hotel_joint()
    )


# Временное уведомление при нажатии кнопок выбора гостиниц.
@router_hotel.callback_query(F.data)
async def handle_button(callback_query: CallbackQuery):
    await callback_query.answer(f'Вы выбрали: {callback_query.data}')
