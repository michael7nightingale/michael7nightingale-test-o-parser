from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def build_menu_keyboard() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup()
    button_1 = KeyboardButton("Список товаров")
    keyboard.add(button_1)
    button_2 = KeyboardButton("Товар")
    keyboard.add(button_2)
    button_3 = KeyboardButton("Парсинг")
    keyboard.add(button_3)
    return keyboard
