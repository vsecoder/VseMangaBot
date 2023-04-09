from aiogram import types
from aiogram.filters import Filter

from app.db.functions import User


class IsOwner(Filter):
    """
    Check if user is owner or not
    """
    def __init__(self, is_owner: bool) -> None:
        self.is_owner = is_owner

    async def __call__(self, message: types.Message) -> bool:
        status = await User.get_status(message.from_user.id)
        return self.is_owner is (status == "admin")
