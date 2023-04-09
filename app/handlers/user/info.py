from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from app.keyboards.inline import get_author_keyboard

from app.filters.is_chat import IsChat

from datetime import datetime

router = Router()


@router.message(Command(commands=["help"]), IsChat(is_chat=False))
async def help_handler(message: Message):
    text = "ℹ️ <b>https://newmanga.org</b>\n\nБот использует данный сайт для парсинга манги и махвы, но вся информация хранится в базе данных бота."
    await message.answer(text)


@router.message(Command(commands=["about"]), IsChat(is_chat=False))
async def about_handler(message: Message, build, upd, start_time):
    link = 'https://github.com/vsecoder/VseMangaBot'
    text = f"📚 <b>VseMangaBot</b> - <a href='{link}'>GitHub</a>\n\n"
    text += f"<b>💫 Version:</b> {upd} #{build[:7]}\n"
    text += f"<b>⌛️ Uptime:</b> {datetime.now() - start_time}"

    await message.answer(
        text,
        reply_markup=get_author_keyboard(),
        disable_web_page_preview=True
    )
