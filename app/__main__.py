import asyncio
import logging
import git

import coloredlogs
from aiogram import Bot, Dispatcher
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.client.telegram import TelegramAPIServer
from aiogram.fsm.storage.memory import MemoryStorage

from app import db, version
from app.arguments import parse_arguments
from app.config import Config, parse_config
from app.db import close_orm, init_orm
from app.handlers import get_handlers_router
from app.middlewares import register_middlewares
from app.commands import remove_bot_commands, setup_bot_commands

from datetime import datetime


async def on_startup(
    dispatcher: Dispatcher, bot: Bot, config: Config
):

    register_middlewares(dp=dispatcher, config=config)

    dispatcher.include_router(get_handlers_router())

    await setup_bot_commands(bot)

    await bot.delete_webhook(
        drop_pending_updates=config.settings.drop_pending_updates,
    )

    tortoise_config = config.database.get_tortoise_config()
    await init_orm(tortoise_config)

    bot_info = await bot.get_me()

    logging.info(f"Name - {bot_info.full_name}")
    logging.info(f"Username - @{bot_info.username}")
    logging.info(f"ID - {bot_info.id}")

    states = {
        True: "Enabled",
        False: "Disabled",
    }

    logging.debug(f"Groups Mode - {states[bot_info.can_join_groups]}")
    logging.debug(f"Privacy Mode - {states[not bot_info.can_read_all_group_messages]}")
    logging.debug(f"Inline Mode - {states[bot_info.supports_inline_queries]}")

    logging.error("Bot started!")


async def on_shutdown(dispatcher: Dispatcher, bot: Bot, config: Config):
    logging.warning("Stopping bot...")
    await remove_bot_commands(bot)
    await bot.delete_webhook(drop_pending_updates=config.settings.drop_pending_updates)
    await dispatcher.fsm.storage.close()
    await bot.session.close()
    await close_orm()


async def main():
    coloredlogs.install(level=logging.INFO)
    logging.warning("Starting bot...")

    arguments = parse_arguments()
    config = parse_config(arguments.config)

    tortoise_config = config.database.get_tortoise_config()
    try:
        await db.create_models(tortoise_config)
    except FileExistsError:
        await db.migrate_models(tortoise_config)

    session = AiohttpSession(
        api=TelegramAPIServer.from_base(
            "https://api.telegram.org",
            is_local=False
        )
    )
    token = config.bot.token
    bot_settings = {"session": session, "parse_mode": "HTML"}

    bot = Bot(token, **bot_settings)
    storage = MemoryStorage()

    dp = Dispatcher(storage=storage)
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    repo = git.Repo()
    print(repo.heads)
    build = repo.heads[0].commit.hexsha if repo.heads else "Not found"
    diff = repo.git.log([f"HEAD..origin/{version.branch}", "--oneline"])
    upd = "Update required" if diff else "Up-to-date"

    start_time = datetime.now()

    context_kwargs = {"config": config, "build": build, "upd": upd, "start_time": start_time}

    await dp.start_polling(bot, **context_kwargs)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.error("Bot stopped!")
