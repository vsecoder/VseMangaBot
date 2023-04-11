from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_author_keyboard():
    buttons = [
        [InlineKeyboardButton(text="@vsecoder", url="https://t.me/vsecoder")],
        [InlineKeyboardButton(text="@sleroq", url="https://t.me/sleroq")],
    ]
    keyboard = InlineKeyboardBuilder(markup=buttons)
    return keyboard.as_markup()


def get_start_keyboard():
    buttons = [
        [InlineKeyboardButton(text="Продолжить", callback_data="continue")],
    ]
    keyboard = InlineKeyboardBuilder(markup=buttons)
    return keyboard.as_markup()


def read_keyboard(slug):
    buttons = [
        [InlineKeyboardButton(text="📖 Читать", callback_data=f"r/{slug}")],
        [InlineKeyboardButton(text="❌ Закрыть", callback_data="close")],
    ]
    keyboard = InlineKeyboardBuilder(markup=buttons)
    return keyboard.as_markup()


def manga_keyboard(data):
    buttons = [
        [
            InlineKeyboardButton(text="Выбор страницы", callback_data=f"pages/{data['id']}/{data['chapter']}/{data['page']}"),
        ],
        [
            InlineKeyboardButton(text="⬅️", callback_data=f"prev/{data['id']}/{data['chapter']}/{data['page']}"),
            InlineKeyboardButton(text="➡️", callback_data=f"next/{data['id']}/{data['chapter']}/{data['page']}")
        ],
        [
            InlineKeyboardButton(text="Выбор главы", callback_data=f"chaptes/{data['id']}/{data['chapter']}/{data['page']}"),
        ],
        [
            InlineKeyboardButton(text="⬅️", callback_data=f"prev_chapter/{data['id']}/{data['chapter']}/{data['page']}"),
            InlineKeyboardButton(text="➡️", callback_data=f"next_chapter/{data['id']}/{data['chapter']}/{data['page']}")
        ]
    ]
    keyboard = InlineKeyboardBuilder(markup=buttons)
    return keyboard.as_markup()


def charaptes_keyboard(slug, chapters):
    chapters = [InlineKeyboardButton(text=f"{i['title']['ru']}", callback_data=f"r/{slug}/") for i in chapters]

    buttons = [
        [
            InlineKeyboardButton(text="Главы:", callback_data="pass")
        ],
        *chapters
    ]
    keyboard = InlineKeyboardBuilder(markup=buttons)
    return keyboard.as_markup()


def search_results_keyboard(data):
    buttons = [
        [
            InlineKeyboardButton(text=i['document']['title_ru'][:60], callback_data=f"i/{i['document']['slug']}")
        ] for i in data if not len(i['document']['slug']) > 61
    ]

    buttons.append(
        [
            InlineKeyboardButton(text="❌ Закрыть", callback_data="close")
        ]
    )

    not_found = [
        [
            InlineKeyboardButton(text="Ничего не найдено", callback_data="pass")
        ]
    ]
    keyboard = InlineKeyboardBuilder(markup=buttons if len(buttons) != 0 else not_found)
    return keyboard.as_markup()
