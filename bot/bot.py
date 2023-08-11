from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
import os
from connector import post_new_chat, get_products, post_run_task, get_product
from parsers import parse_products_list, parse_product

bot = Bot(token=os.getenv("TOKEN"))
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


class States(StatesGroup):
    N = State()
    ID = State()


@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    status, response = post_new_chat(message.chat.id)
    if status == 200:
        response_text = "Hello!"
    else:
        response_text = "You have already started bot or something went wrong with the request."
    await message.answer(response_text)


@dp.message_handler(commands=["goods"])
async def good_list(message: types.Message):
    status, products = get_products(message.chat.id)
    if status == 200:
        response_text = parse_products_list(products)
    else:
        response_text = products
    await message.answer(response_text)


@dp.message_handler(commands=["retrieve"])
async def good_retrieve(message: types.Message):
    await States.ID.set()
    await message.answer("Input product id")


@dp.message_handler(state=States.ID)
async def process_id(message: types.Message):
    id_ = message.text
    status, product = get_product(id)
    if status == 200:
        response_text = parse_product(product)
    else:
        response_text = product
    await message.answer(response_text)


@dp.message_handler(commands=["run_task"])
async def run_group_task(message: types.Message):
    await States.N.set()
    await message.answer("Input the amount of pages from 1 to 50.")


@dp.message_handler(state=States.N)
async def process_n(message: types.Message):
    n = message.text
    if n and n.isnumeric():
        n = int(n)
        if 1 <= n <= 50:
            post_run_task(n, message.chat.id)
            await message.answer(f"Your task to parse {n} pages is started.")
            return
    await message.answer("Integer from 1 to 50 is expected.")


async def serve_forever():
    await dp.start_polling(bot)
