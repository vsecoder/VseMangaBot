from aiogram import types
from aiogram.filters import Filter


class IsChat(Filter):
    """
    Check if message is chat or not
    """
    def __init__(self, is_chat: bool) -> None:
        self.is_chat = is_chat

    async def __call__(self, message: types.Message) -> bool:
        return (message.chat.id != message.from_user.id) is self.is_chat
