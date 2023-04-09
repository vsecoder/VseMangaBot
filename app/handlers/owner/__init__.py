from aiogram import Router


def get_owner_router() -> Router:
    from . import statistics, stuff, mailing

    router = Router()
    router.include_router(statistics.router)
    router.include_router(stuff.router)
    router.include_router(mailing.router)

    return router
