from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
import user.keyboards.keyboards as kb
import user.keyboards.keyboards_hotel as kb_hotel
from user.handlers.handlers import Form

router_hotel = Router()  # Создание объекта.


@router_hotel.callback_query(F.data == 'Buta')
async def get_callback_query_hotel_buta(callback: CallbackQuery,
                                        state: FSMContext):
    await state.set_state(Form.waiting_for_hotel_details)
    await callback.message.edit_text(
        text='Вы выбрали <b><u>Отель Buta</u></b>',
        parse_mode=ParseMode.HTML,
        reply_markup=await kb_hotel.build_button_places_hotel_joint()
    )


@router_hotel.callback_query(F.data == 'IT Time')
async def get_callback_query_hotel_it_time(callback: CallbackQuery,
                                           state: FSMContext):
    await state.set_state(Form.waiting_for_hotel_details)
    await callback.message.edit_text(
        text='Вы выбрали <b><u>Отель IT Time</u></b>',
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
        reply_markup=kb.inline_list_places
    )


# Обработка при нажатии кн.' Подробнее'.
@router_hotel.callback_query(F.data == 'Подробнее')
async def handle_more_details(callback: CallbackQuery):
    # Отправляем сообщение с подробной информацией
    await callback.message.answer(
        'Здесь будет подробная информация об отеле.'
    )
    # Подтверждаем обработку callback-запроса.
    await callback.answer()


# Обработка при нажатии кн.'Назад'.
@router_hotel.callback_query(F.data == 'back_hotel')
async def handle_back_button(callback: CallbackQuery, state: FSMContext):
    await callback.answer()  # Очищаем уведомление.

    # Возврат в состояние выбора Гостиница.
    await state.set_state(Form.waiting_for_hotel_details)

    await callback.message.edit_text(
        text='Вы выбрали раздел <b><u>Гостиница</u></b>',
        parse_mode=ParseMode.HTML,

        # Подключение Inline-клавиатуры со списком гостиниц.
        reply_markup=await kb_hotel.build_button_places_hotel()
    )


# Временное уведомление при нажатии кнопок выбора гостиниц.
@router_hotel.callback_query(F.data)
async def handle_button(callback_query: CallbackQuery):
    await callback_query.answer(f'Вы выбрали: {callback_query.data}')
