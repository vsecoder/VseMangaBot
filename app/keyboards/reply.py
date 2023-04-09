from aiogram import types


async def main_menu():
    buttons = [
        [
            types.KeyboardButton(text="📊 Топ"),
            types.KeyboardButton(text="🗳 Поиск")
        ],
        [
            types.KeyboardButton(text="📍 Избранное")
        ],
        [
            types.KeyboardButton(text="📎 Продолжить читать")
        ]
    ]

    keyboard = types.ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
    return keyboard
