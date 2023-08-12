from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
import os
from connector import post_new_chat, get_products, post_run_task, get_product
from keyboards import build_menu_keyboard
from parsers import parse_products_list, parse_product


# bot instance and configurations
bot = Bot(token=os.getenv("TOKEN"))
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


class States(StatesGroup):
    """Bot state class."""
    N = State()
    ID = State()


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    """Start handler to register new chat_id."""
    reply_markup = build_menu_keyboard()
    await register(message, reply_markup=reply_markup)


@dp.message_handler(Text(equals="Регистрация"))
async def register(message: types.Message, reply_markup=None):
    """Register handler to register new chat_id."""
    status, response = post_new_chat(message.chat.id)
    if status == 200:
        response_text = "Hello!"
    else:
        response_text = "You have already started bot or something went wrong with the request."
    if reply_markup:
        await message.answer(response_text, reply_markup=reply_markup)
    else:
        await message.answer(response_text)


@dp.message_handler(Text(equals="Список товаров"))
async def good_list(message: types.Message):
    """Good list handler. Get the last products from the last parsing task."""
    status, products = get_products(message.chat.id)
    if status == 200:
        response_text = parse_products_list(products, message.chat.id)
    else:
        response_text = products
    await message.answer(response_text)


@dp.message_handler(Text(equals="Товар"))
async def good_retrieve(message: types.Message):
    """Get a single god."""
    await States.ID.set()
    await message.answer("Input product id")


@dp.message_handler(state=States.ID)
async def process_id(message: types.Message, state: FSMContext):
    """Process good id input."""
    id_ = message.text
    status, product = get_product(id_)
    if status == 200:
        response_text = parse_product(product)
    else:
        response_text = product
    await state.finish()
    await message.answer(response_text)


@dp.message_handler(Text(equals="Парсинг"))
async def run_group_task(message: types.Message):
    """Handler for running parsing task"""
    await States.N.set()
    await message.answer("Input the amount of pages from 1 to 50.")


@dp.message_handler(state=States.N)
async def process_n(message: types.Message, state: FSMContext):
    """Process `n_page` input handler."""
    n = message.text
    wrong_answer_delegate = message.answer("Integer from 1 to 50 is expected.")
    if n and n.isnumeric():
        n = int(n)
        if 1 <= n <= 50:
            post_run_task(n, message.chat.id)
            await state.finish()
            await message.answer(f"Your task to parse {n} pages is started.")
            return
    await state.finish()
    await wrong_answer_delegate


async def serve_forever():
    """Function to run telegram bot."""
    await dp.start_polling(bot)
