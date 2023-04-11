from aiogram import Router, Bot, types
from aiogram.types import CallbackQuery
from app.keyboards.reply import main_menu
from app.db.functions import User, _

from app.keyboards.inline import read_keyboard, manga_keyboard

from app.api.newmanga import API

router = Router()


async def info(c: CallbackQuery, bot: Bot):
    await c.answer("Инициализация...")
    slug = c.data.split('/')[1]
    desc = await API().get_manga_info(slug)
    text = f"<b>{desc['title']['ru']}</b><a href=\"https://img.newmanga.org/ProjectCard/webp/{desc['image']['name']}\">.</a>" \
        f"\n🌟 Рейтинг: {round(desc['rating'], 1)}\n\n<i>{desc['description']}</i>"
    return await bot.send_message(c.from_user.id, text, reply_markup=read_keyboard(slug))


async def read(c: CallbackQuery, bot: Bot):
    await c.answer("Инициализация...")
    slug = c.data.split('/')[1]
    manga_info = await API().get_manga_info(slug)
    manga_id = manga_info['branches'][0]['id']

    chapters = (await API().get_chapters(manga_id))
    chapter_id = chapters[0]['id']
    pages = (await API().get_pages(chapter_id))
    page = pages['pages'][0]

    data = {
        "id": manga_id,
        "chapter": 0,
        "page": 0,
    }

    img = await API().get_image_url(pages['origin'], chapter_id, page['slices'][0]['path'])

    return await bot.send_photo(
        c.from_user.id,
        img,
        caption=f"<b>📙 {manga_info['title']['ru']}</b>\n\n📖 Глава: {data['chapter']+1}/{len(chapters)}\n📄 Страница: {data['page']+1}/{len(pages['pages'])}",
        reply_markup=manga_keyboard(data)
    )

async def move(c: CallbackQuery, bot: Bot):
    args = c.data.split('/')
    data = {
        "action": args[0],
        "id": args[1],
        "chapter": int(args[2]),
        "page": int(args[3]),
    }

    chapters = (await API().get_chapters(data['id']))

    if data['action'] == "next":
        data['page'] += 1
    elif data['action'] == "prev":
        if data['page'] == 0:
            return await c.answer("Это первая страница!")
        data['page'] -= 1
    elif data['action'] == "next_chapter":
        if data['chapter'] == len(chapters):
            return await c.answer("Это последняя глава!")
        data['chapter'] += 1
        data['page'] = 0
    elif data['action'] == "prev_chapter":
        if data['chapter'] == 0:
            return await c.answer("Это первая глава!")
        data['chapter'] -= 1
        data['page'] = 0
    
    chapter = chapters[data['chapter']]
    chapter_id = chapter['id']
    pages = (await API().get_pages(chapter_id))
    page = pages['pages'][data['page']]
    
    if data['page'] > len(pages['pages']):
        return await c.answer("Это последняя страница!")
    
    img = await API().get_image_url(pages['origin'], chapter_id, page['slices'][0]['path'])

    await c.message.delete()

    return await bot.send_photo(
        c.from_user.id,
        img,
        caption=f"<b>📖 Глава:</b> {data['chapter']+1}/{len(chapters)}\n<b>📄 Страница:</b> {data['page']+1}/{len(pages['pages'])}",
        reply_markup=manga_keyboard(data)
    )

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
    
    if not '/' in c.data:
        return
    
    action = c.data.split('/')[0]
    actions = {
        "i": info,
        "r": read,
        "next": move,
        "prev": move,
        "next_chapter": move,
        "prev_chapter": move,
    }

    if action in actions:
        return await actions[action](c, bot)