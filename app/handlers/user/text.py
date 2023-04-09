from aiogram import Router
from aiogram.types import Message

from app.db.functions import User

from app.filters.is_chat import IsChat

from aiogram_dialog import DialogManager

from app.dialogs.popular_dialog import PopularDialog

#from app.api.newmanga import API

router = Router()


@router.message(IsChat(is_chat=False))
async def text_handler(message: Message, dialog_manager: DialogManager):
    if not await User.is_registered(message.from_user.id):
        return
    
    if await User.get_status(message.from_user.id) != "reader":
        return
    
    if message.text == '📊 Топ':
        await dialog_manager.start(PopularDialog.top_list)

    elif message.text == '🗳 Поиск':
        pass

    elif message.text == '📍 Избранное':
        pass

    elif message.text == '📎 Продолжить читать':
        pass
