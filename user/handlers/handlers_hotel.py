from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
import user.keyboards.keyboards as kb
import user.keyboards.keyboards_hotel as kb_hotel
from user.handlers.handlers import Form

router_hotel = Router()  # Создание объекта.


# Обработка кнопок выбора названий Гостиниц.
@router_hotel.callback_query(F.data.startswith('hotel_'))
async def get_callback_query_hotel_it_time(callback: CallbackQuery,
                                           state: FSMContext):
    # Извлекаем название гостиницы.
    hotel_name = callback.data.replace('hotel_', '')

    # Сохраняем название гостиницы в состоянии.
    await state.update_data(hotel_name=hotel_name)

    # Устанавливаем состояние.
    await state.set_state(Form.waiting_for_hotel_details)

    # Отправляем сообщение с выбранным названием гостиницы.
    await callback.message.edit_text(
        text=f'Вы выбрали <b><u>{hotel_name}</u></b>',
        parse_mode=ParseMode.HTML,
        reply_markup=await kb_hotel.build_button_places_hotel_joint()
    )


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
    hotel_name = data.get('hotel_name', 'неизвестная гостиница')

    # Отправляем сообщение с подробной информацией.
    await callback.message.edit_text(
        text=f'Здесь будет информация об отеле <b><u>{hotel_name}</u></b>.',
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
    hotel_name = data.get('hotel_name', 'неизвестная гостиница')

    # Возврат к предыдущему сообщению.
    await callback.message.edit_text(
        text=f'Вы вернулись к выбранной гостинице <b><u>{hotel_name}</u></b>',
        parse_mode=ParseMode.HTML,

        # Подключаем кнопки под выбранной Гостиницей.
        reply_markup=await kb_hotel.build_button_places_hotel_joint()
    )


# Временное уведомление при нажатии кнопок выбора гостиниц.
@router_hotel.callback_query(F.data)
async def handle_button(callback_query: CallbackQuery):
    await callback_query.answer(f'Вы выбрали: {callback_query.data}')
