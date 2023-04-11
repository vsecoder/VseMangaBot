from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery
from aiogram_dialog import Dialog, DialogManager, Window
from aiogram_dialog.widgets.kbd import Button


class ChangeChapterDialog(StatesGroup):
    chapters = State()


async def show_alert(c: CallbackQuery, _: Button, manager: DialogManager):
    pass

async def get_top(**kwargs):
    pass


ui = Dialog(
    Window(
    ),
)
