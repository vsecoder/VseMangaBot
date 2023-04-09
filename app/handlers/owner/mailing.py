from aiogram import Bot, Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.exceptions import TelegramAPIError

from app.filters.is_owner import IsOwner
from app.db.functions import User

router = Router()


@router.message(IsOwner(is_owner=True), Command(commands=["mail"]))
async def mail_handler(message: Message, bot: Bot):
    users = await User.all()
    geted = 0
    text = message.text.split(maxsplit=1)[1]
    await message.answer(f"✅ Рассылка начата! Всего: {len(users)}")

    for user in users:
        try:
            await bot.send_message(user.telegram_id, text, disable_web_page_preview=True)
            geted += 1
        except TelegramAPIError:
            pass

    await message.answer(f"✅ Рассылка завершена! Получили: {geted}")
