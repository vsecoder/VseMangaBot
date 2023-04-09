from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery
from aiogram_dialog import Dialog, DialogManager, Window
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Const, Format

from app.keyboards.inline import read_keyboard

from app.api.newmanga import API


class PopularDialog(StatesGroup):
    top_list = State()


async def show_alert(c: CallbackQuery, _: Button, manager: DialogManager):
    if c.data == "exit":
        await manager.done()
        await c.message.delete()
        return

    top = await API().get_popular(5)
    data = top[int(c.data)-1]
    
    badge = '🥇' if top.index(data) == 0 else '🥈' if top.index(data) == 1 else '🥉' if top.index(data) == 2 else '🏅'
    await c.message.delete()
    await c.message.answer(
        f"<b>{badge} {data['title']['ru']}</b><a href=\"https://img.newmanga.org/ProjectCard/webp/{data['image']['name']}\">.</a>" \
            f"\n🌟 Рейтинг: {round(data['rating'], 1)}\n\n<i>{data['description']}</i>",
        reply_markup=read_keyboard(data['slug']),
    )
    await manager.done()

async def get_top(**kwargs):
    top = await API().get_popular(5)
    return {
        "title_1": top[0]["title"]['ru'],
        "title_2": top[1]["title"]['ru'],
        "title_3": top[2]["title"]['ru'],
        "title_4": top[3]["title"]['ru'],
        "title_5": top[4]["title"]['ru'],
    }


ui = Dialog(
    Window(
        Const("<b>Топ по прочтениям:</b>"),
        Button(Format("{title_1}"), id="1", on_click=show_alert),
        Button(Format("{title_2}"), id="2", on_click=show_alert),
        Button(Format("{title_3}"), id="3", on_click=show_alert),
        Button(Format("{title_4}"), id="4", on_click=show_alert),
        Button(Format("{title_5}"), id="5", on_click=show_alert),
        Button(Const("◀️ Назад"), id="exit", on_click=show_alert),

        state=PopularDialog.top_list,
        getter=get_top,
    ),
)
