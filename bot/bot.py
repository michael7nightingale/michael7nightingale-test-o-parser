from aiogram import Bot, Dispatcher, types
import os
from connector import post_new_chat, get_products, post_run_task


bot = Bot(token=os.getenv("TOKEN"))
dp = Dispatcher(bot)


@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    post_new_chat(message.chat.id)
    await message.answer("Hello!")


@dp.message_handler(commands=["goods"])
async def good_list(message: types.Message):
    products = get_products()
    await message.answer(products)


@dp.message_handler(commands=["run_task"])
async def good_retrieve(message: types.Message):
    await message.answer("Input the amount of pages from 1 to 50.")


async def serve_forever():
    await dp.start_polling(bot)
