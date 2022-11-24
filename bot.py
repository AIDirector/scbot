import logging
import os
import re
from _ast import Call

import aiohttp
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.files import JSONStorage
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto

from database import UsersTable, EmployeesTable, BooksTable, FilesTable
from messages import messages as msgs, keyboards as kbs
from settings import API_TOKEN, NEED_SAVE_LOGS_TO_FILE

from model import get_intent

# Configure logging

if NEED_SAVE_LOGS_TO_FILE:
    logging.basicConfig(filename="zdravbot.log",
                        filemode='a',
                        format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                        datefmt='%H:%M:%S',
                        level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.DEBUG)

# Initialize bot and dispatcher

storage = JSONStorage("storage.json")

if "https_proxy" in os.environ:
    proxy_url = os.environ["https_proxy"]
    bot = Bot(token=API_TOKEN, proxy=proxy_url)
else:
    bot = Bot(token=API_TOKEN)

dp = Dispatcher(bot, storage=storage)


class States(StatesGroup):
    main_state = State()
    registered_state = State()
    registration_waiting_medical_policy_state = State()
    registration_waiting_phone_state = State()
    registration_waiting_email_state = State()
    book_employee_waiting_day_state = State()
    book_employee_waiting_time_state = State()
    book_employee_waiting_accept_state = State()


@dp.message_handler(commands=['start', 'help'], state="*")
async def send_welcome(message: types.Message, state: FSMContext):
    telegram_id = message.from_user.id
    user = UsersTable.get_or_none(telegram_id=telegram_id)

    if user is None:
        await States.registration_waiting_medical_policy_state.set()
        await message.reply(msgs.get_message("hello"))
        await message.answer(msgs.get_message("registration_start"))
        logging.info(f"Message from {message.from_user.username}: {message.text}")
    else:
        await States.registered_state.set()
        markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True) \
            .add("Войти", "Удалить аккаунт")
        await message.reply(msgs.get_message("registered"), reply_markup=markup)


@dp.message_handler()
async def echo_handler(message: types.Message):
    await message.answer("ECHO")
    await message.answer(message.text)


@dp.message_handler(state=States.registered_state)
async def handle_registered(message: types.Message, state: FSMContext):
    if message.text == "Удалить аккаунт":
        telegram_id = message.from_user.id
        UsersTable.delete_user_by_telegram_id(telegram_id)
        await States.registration_waiting_medical_policy_state.set()
        await message.reply(msgs.get_message("hello"))
        await message.answer(msgs.get_message("registration_start"))
        logging.info(f"Message from {message.from_user.username}: {message.text}")
    else:
        await state.finish()
        await States.main_state.set()
        await message.reply(msgs.get_message("hello"), reply_markup=kbs.get_keyboard('main_keyboard'))


@dp.message_handler(state=States.registration_waiting_medical_policy_state)
async def registration_medical_policy_state_handle(message: types.Message, state: FSMContext):
    try:
        medical_policy = int(message.text)
    except ValueError:
        await message.answer(msgs.get_message("registration_medical_policy_failed"))
        return

    async with state.proxy() as data:
        data["medical_policy"] = medical_policy

    await message.answer(msgs.get_message("registration_medical_policy_ok"))
    await message.answer(msgs.get_message("registration_get_phone"))
    await States.registration_waiting_phone_state.set()


@dp.message_handler(state=States.registration_waiting_phone_state)
async def registration_phone_state_handle(message: types.Message, state: FSMContext):
    if re.fullmatch("\+?[78]\s?\(?\d{3}\)?\s?([-\s]?\d[-\s]?){7}", message.text):
        phone = '7' + re.sub("\D", "", message.text)[-10:]

        async with state.proxy() as data:
            data["phone"] = phone

        await message.answer(msgs.get_message("registration_phone_ok"))
        await message.answer(msgs.get_message("registration_get_email"))
        await States.registration_waiting_email_state.set()
    else:
        await message.answer(msgs.get_message("registration_phone_failed"))


@dp.message_handler(state=States.registration_waiting_email_state)
async def registration_email_state_handle(message: types.Message, state: FSMContext):
    if re.fullmatch(".+@.+", message.text):
        async with state.proxy() as data:
            data["email"] = message.text

        await message.answer(msgs.get_message("registration_email_ok"))
        async with state.proxy() as data:
            UsersTable.create(user_name=f"{message.from_user.first_name} {message.from_user.last_name}",
                              telegram_id=message.from_user.id, phone_number=data["phone"],
                              email=data["email"], medical_policy=data["medical_policy"])
        await state.finish()
        await States.main_state.set()
        await message.answer(msgs.get_message("intro"), reply_markup=kbs.get_keyboard('main_keyboard'))
    else:
        await message.answer(msgs.get_message("registration_email_failed"))


@dp.message_handler(state=States.main_state)
async def main_state_handler(message: types.Message, state: FSMContext):
    intent = get_intent(message.text)
    if intent != "UNKNOWN":
        await message.answer(intent)
    else:
        await message.answer("СОВСЕМ НЕПОНЯТНО")

    if re.fullmatch(".*(врач|специалист|доктор).*", message.text.lower()):
        for employee in EmployeesTable.all_employees():
            keyboard = InlineKeyboardMarkup() \
                .add(InlineKeyboardButton("Записаться", callback_data=f"book_employee_{employee.employee_id}"))

            async def send_file(file):
                result = await message.answer_photo(
                    file,
                    caption=f'{employee.type.display_name} {employee.name}',
                    reply_markup=keyboard
                )
                return result.photo[0].file_id

            await FilesTable.do_action_with_file(employee.photo_filename, send_file)

    elif re.fullmatch(".*(запис(ь|аться)).*", message.text.lower()):
        pass
    elif re.fullmatch(".*(инфо).*", message.text.lower()):
        filenames = []
        for employee in EmployeesTable.all_employees():
            filenames.append(employee.photo_filename)

        messages = ["1", "2", "3", "4"]

        async def send_mediagroup(_files):
            files = []
            for file in _files:
                files.append(InputMediaPhoto(file, messages.pop()))

            await bot.send_media_group(
                message.from_user.id,
                files,

            )

        await FilesTable.do_action_with_files(filenames, send_mediagroup)



    elif re.fullmatch(".*(мои\sзаписи).*", message.text.lower()):
        for book in BooksTable.books_by_user_telegram_id(message.from_user.id):
            book: BooksTable = book
            await message.answer(f"{book.employee.name}, {book.day} {book.time}")
    else:
        await message.reply(msgs.get_message("not_understand"))


@dp.callback_query_handler(state=States.main_state, text_startswith="book_employee_")
async def book_employee_handler(call: types.CallbackQuery, state: FSMContext):
    employee_id = int(call.data.split('_')[2])
    employee = EmployeesTable.get(EmployeesTable.employee_id == employee_id)
    async with state.proxy() as data:
        data['employee_id'] = employee_id

    await States.book_employee_waiting_day_state.set()

    await call.message.answer(
        msgs.get_message("book_employee_start", employee_name=employee.name),
        reply_markup=kbs.get_keyboard("choose_day_keyboard")
    )

    await call.answer()


@dp.message_handler(text="Отменить", state=(States.book_employee_waiting_time_state,
                                            States.book_employee_waiting_accept_state,
                                            States.book_employee_waiting_day_state))
async def cancel_book_employee(message: types.Message, state: FSMContext):
    await state.finish()
    await States.main_state.set()
    await message.answer(msgs.get_message('cancel_book_employee'), reply_markup=kbs.get_keyboard('main_keyboard'))


@dp.message_handler(state=States.book_employee_waiting_day_state)
async def book_employee_waiting_day_state_handler(message: types.Message, state: FSMContext):
    if message.text in ("Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота"):
        async with state.proxy() as data:
            data['book_day'] = message.text
        await message.answer(msgs.get_message("book_employee_day_ok"),
                             reply_markup=kbs.get_keyboard("choose_time_keyboard"))
        await States.book_employee_waiting_time_state.set()
    else:
        await message.answer(msgs.get_message("book_employee_day_fail"))


@dp.message_handler(state=States.book_employee_waiting_time_state)
async def book_employee_waiting_time_state_handler(message: types.Message, state: FSMContext):
    if re.fullmatch("\d{1,2}:\d{1,2}", message.text):
        async with state.proxy() as data:
            data['book_time'] = message.text
            employee = EmployeesTable.get(EmployeesTable.employee_id == data['employee_id'])

            await message.answer(
                msgs.get_message("book_data_request_accept", employee_name=employee.name,
                                 book_day=data['book_day'], book_time=data['book_time']),
                reply_markup=kbs.get_keyboard("accept_keyboard"))
        await States.book_employee_waiting_accept_state.set()
    else:
        await message.answer(msgs.get_message("book_employee_day_fail"))


@dp.message_handler(state=States.book_employee_waiting_accept_state)
async def book_employee_waiting_time_state_handler(message: types.Message, state: FSMContext):
    if message.text.lower() == "принять":
        user = UsersTable.from_telegram_id(message.from_user.id)
        async with state.proxy() as data:
            employee = EmployeesTable.get(EmployeesTable.employee_id == data['employee_id'])
            BooksTable.create(user=user, employee=employee, day=data["book_day"], time=data["book_time"])
        await message.answer(msgs.get_message("book_data_ok"), reply_markup=kbs.get_keyboard("main_keyboard"))
        await state.finish()
        await States.main_state.set()

        async with aiohttp.ClientSession() as session:
            async with session.post('http://127.0.0.1:8080/send',
                                    json={"id": 10, "ok": True, "secret": "Some_secret"}) as resp:
                print(resp.status)
                print(await resp.text())

    else:
        await message.answer(msgs.get_message("not_understand"))

