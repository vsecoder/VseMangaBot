from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from app.db.functions import User, _
from app.keyboards.inline import get_start_keyboard
from app.keyboards.reply import main_menu

from app.filters.is_chat import IsChat

router = Router()


@router.message(CommandStart(), IsChat(is_chat=False))
async def cmd_start(message: Message):
    user_id = message.from_user.id

    if not await User.is_registered(user_id):
        await User.register(
            user_id,
            name=_(message.from_user.full_name),
        )

    if await User.get_status(user_id) == "reader":
        return await message.answer(
            "📚 Клавиатура активирована!",
            reply_markup=await main_menu(),
        )

    await message.answer_sticker(
        sticker="CAACAgIAAxkBAAEfev5kMuRvBIKD0jlBZ8TACdUWmOlO5wACVAMAAlX9MBHtWPZRU3DkBi8E"
    )

    await message.answer(
        f"<b>🍅 Привет тебе странник!</b>\n\n"
        "В боте:\n"
        " - <i>можно читать мангу, манхву и маньхуа</i>;\n"
        " - <i>всё в удобном формате</i>;\n"
        " - <i>есть автосохранение прогресса</i>;\n"
        " - <i>есть закладки и история</i>;\n"
        " - <i>а главное - наличае поиска</i>.\n\n"
        "<b>⚠️ Продолжая вы соглашаетсь с правилами конфиденциальности!</b>",
        reply_markup=get_start_keyboard(),
    )
