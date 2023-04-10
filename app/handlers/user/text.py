from aiogram import Router
from aiogram.types import Message

from app.db.functions import User, _

from app.filters.is_chat import IsChat

from aiogram_dialog import DialogManager
from app.dialogs.popular_dialog import PopularDialog

from app.api.newmanga import API

from app.keyboards.inline import search_results_keyboard

router = Router()


@router.message(IsChat(is_chat=False))
async def text_handler(message: Message, dialog_manager: DialogManager):
    if not await User.is_registered(message.from_user.id):
        return
    
    if await User.get_status(message.from_user.id) == "user":
        return
    
    if message.text == '📊 Топ':
        await dialog_manager.start(PopularDialog.top_list)

    elif message.text == '🗳 Поиск':
        return await message.answer("<b>Введите текст для поиска:</b>")

    elif message.text == '📍 Избранное':
        pass

    elif message.text == '📎 Продолжить читать':
        pass

    else:
        search = (await API().search(message.text, 1, 5))['result']['hits']
        await message.answer(
            f"🔍 <b>Результаты поиска по запросу:</b>\n\n<code>{_(message.text)}</code>",
            reply_markup=search_results_keyboard(search)
        )
