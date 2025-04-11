import random
import re
import string

from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder

import user.keyboards.keyboards as kb
import user.keyboards.keyboards_hotel as kb_hotel
from database.database_postgresql import (
    get_prices_from_db, get_id_hotel_and_price_and_description_from_db,
    save_user, get_hotel_id_from_db)
from user.handlers.handlers import Form

from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message

router_hotel = Router()  # Создание объекта.


class ProfileReg(StatesGroup):
    name = State()
    phone_number = State()
    email = State()


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
        reply_markup=await kb_hotel.build_button_places_hotel_joint(),
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
        text='Вы перешли в раздел <b><u>выбора мест отдыха:</u></b>',
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
        reply_markup=await kb_hotel.build_button_places_hotel(),
    )


# Обработка при нажатии кн. "Подробнее".
@router_hotel.callback_query(F.data == 'Подробнее')
async def handle_more_details(callback: CallbackQuery, state: FSMContext):
    # Извлекаем название гостиницы из состояния.
    data = await state.get_data()
    hotel_name = data.get('hotel_name', 'неизвестный отель')

    # Получаем данные о гостинице через подключение к бд.
    hotels_and_prices = await get_id_hotel_and_price_and_description_from_db()
    hotel_description = next(
        (
            hotel['description']
            for hotel in hotels_and_prices
            if hotel['name'] == hotel_name
        ),
        None,
    )

    # Обрабатываем ошибку, когда нет информации о выбранной гостинице.
    if not hotel_description:
        await callback.answer(
            text='Ошибка: Описание для гостиницы не найдено или недоступно.',
            show_alert=True,  # Всплывающее сообщение.
        )
        return

    await callback.message.edit_text(
        text=f'Описание отеля <b><u>{hotel_name}</u></b>: {hotel_description}',
        parse_mode=ParseMode.HTML,
        # Подключаем кнопку "Назад".
        reply_markup=kb_hotel.get_back_button(),
    )
    # Подтверждаем обработку callback-запроса.
    await callback.answer()


# Обработка при нажатии кн."Цена".
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
        await callback.answer(
            text='Ошибка: Цена для отеля не найдена.',
            show_alert=True
        )
        return

    # Отправляем сообщение с информацией о цене.
    await callback.message.edit_text(
        text=f'Цена в отеле <b><u>{hotel_name}</u></b>: <b>{hotel_price}</b> ' 
             f'руб.',
        parse_mode=ParseMode.HTML,
        # Подключаем кнопку "Назад".
        reply_markup=kb_hotel.get_back_button(),
    )
    # Подтверждаем обработку callback-запроса.
    await callback.answer()


# Удаление сообщений после ввода данных в разделе 'Забронировать'.
async def delete_messages(messages):
    for msg in messages:
        try:
            await msg.delete()
        except Exception as e:
            print(f'Ошибка при удалении сообщения: {e}')


# Обработка при нажатии кн. 'Забронировать'.
@router_hotel.callback_query(F.data == 'Забронировать')
async def start_booking(callback: CallbackQuery, state: FSMContext):
    # Извлекаем hotel_name из состояния.
    user_data = await state.get_data()
    hotel_name = user_data.get('hotel_name')

    # Получаем hotel_id по названию отеля.
    hotel_id = await get_hotel_id_from_db(hotel_name)

    # Сохраняем hotel_id в состоянии.
    await state.update_data(hotel_id=hotel_id)

    # Переходим в состояние ожидания ввода имени.
    await state.set_state(ProfileReg.name)

    # Сохраняем идентификатор сообщения, которое мы редактируем.
    message = await callback.message.edit_text(
        text='Введите <b><u>ваше имя:</u></b>',
        parse_mode=ParseMode.HTML
    )

    # Инициализируем список сообщений.
    await state.update_data(messages=[message])
    await callback.answer()


# Обработка ввода имени.
@router_hotel.message(ProfileReg.name)
async def process_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)

    # Получаем данные из состояния.
    user_data = await state.get_data()

    # Извлекаем список сообщений.
    messages = user_data.get('messages', [])

    # Удаляем сообщение.
    await delete_messages(messages)

    # Переходим в состояние ожидания ввода номера телефона.
    new_bot_message = await message.answer(
        text='Введите ваш <b><u>номер телефона:</u></b>',
        parse_mode=ParseMode.HTML
    )
    # Создание списка сообщений:
    messages = [new_bot_message, message]

    # Обновление данных состояния:
    await state.update_data(messages=messages)

    # Установка нового состояния.
    await state.set_state(ProfileReg.phone_number)


# Обработка ввода номера телефона.
@router_hotel.message(ProfileReg.phone_number)
async def process_phone(message: Message, state: FSMContext):
    # Удаляем все символы, кроме цифр.
    phone = re.sub(r'[^0-9]', '', message.text)

    # Проверяем номер телефона на содержание цифр установленной длины.
    if not phone.isdigit() or len(phone) != 12:
        await message.answer(
            text='Номер телефона должен содержать <b><u>только цифры и быть'
            ' не короче 12 символов.</u></b>',
            parse_mode=ParseMode.HTML,
        )
        return

    await state.update_data(phone_number=phone)

    user_data = await state.get_data()
    messages = user_data.get('messages', [])

    # Удаляем предыдущие сообщения.
    await delete_messages(messages)

    # Переходим в состояние ожидания ввода email.
    new_bot_message = await message.answer(
        text='Введите ваш <b><u>действующий email:</u></b>',
        parse_mode=ParseMode.HTML
    )

    # Сохраняем последние сообщения.
    messages = [new_bot_message, message]
    await state.update_data(messages=messages)

    await state.set_state(ProfileReg.email)


# Обработка ввода email.
@router_hotel.message(ProfileReg.email)
async def process_email(message: Message, state: FSMContext):
    email = message.text

    # Проверяем email на валидность по шаблону.
    if not re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$',
                    email):
        await message.answer(
            text='Введите <b><u>корректный email.</u></b>',
            parse_mode=ParseMode.HTML
        )
        return

    await state.update_data(email=email)
    user_data = await state.get_data()
    messages = user_data.get('messages', [])

    # Добавляем последнее сообщение от пользователя.
    messages.append(message)

    # Удаляем все сообщения.
    await delete_messages(messages)

    # Вызываем функцию завершения бронирования
    await finish_booking(message, state)


# Завершение бронирования.
async def finish_booking(message: Message, state: FSMContext):
    # Извлекаем данные из состояния.
    user_data = await state.get_data()

    # Генерирование кода (буквы верхнего и нижнего регистра + цифры).
    code_generation = string.ascii_letters + string.digits

    # Генерируем номер бронирования.
    user_data['booking_number'] = (
        f"HOTEL-{user_data['hotel_id']}-"
        f"{''.join(random.choices(code_generation, k=10))}"
    )

    # Сохранение данных от пользователя в словарь.
    await save_user(user_data)

    try:
        # Создаем клавиатуру с кн."В главное меню".
        keyboard = InlineKeyboardBuilder()
        keyboard.row(kb_hotel.create_main_menu_button())

        await message.answer(
            text=f'Спасибо! Ваши данные сохранены.\n'
            f'Бронирование успешно оформлено! Номер бронирования: \n'
            f'<b><u>{user_data["booking_number"]}</u></b>',
            parse_mode=ParseMode.HTML,

            # Подключение кн. "В главное меню".
            reply_markup=keyboard.as_markup()
        )
    except Exception as e:
        await message.answer(f'Ошибка при бронировании: {e}')
    finally:
        await state.clear()


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
        reply_markup=await kb_hotel.build_button_places_hotel_joint(),
    )


# Временное уведомление при нажатии кнопок выбора гостиниц.
@router_hotel.callback_query(F.data)
async def handle_button(callback_query: CallbackQuery):
    await callback_query.answer(f'Вы выбрали: {callback_query.data}')
