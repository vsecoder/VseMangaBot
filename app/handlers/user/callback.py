from aiogram import Router, Bot
from aiogram.types import CallbackQuery
from app.keyboards.reply import main_menu
from app.db.functions import User, _

router = Router()


@router.callback_query()
async def continue_use(c: CallbackQuery, bot: Bot):
    if c.data == "continue":
        await User.set_status(c.from_user.id, "reader")
        await bot.send_message(
            c.from_user.id,
            "📚 Клавиатура активирована!",
            reply_markup=await main_menu(),
        )
        await c.message.delete()

    elif c.data == "close":
        await c.message.delete()

    elif c.data == "pass":
        return
