from typing import Union

from tortoise.exceptions import DoesNotExist

from app.db import models


def _(text):
    return text.replace('<', '').replace('>', '')


class User(models.User):
    """
    User model, contains all methods for working with users.
    """
    @classmethod
    async def is_registered(cls, telegram_id: int) -> Union[models.User, bool]:
        try:
            return await cls.get(telegram_id=telegram_id)
        except DoesNotExist:
            return False

    @classmethod
    async def register(
        cls,
        telegram_id,
        name
    ):
        await User(
            telegram_id=telegram_id,
            name=name,
            status="user",
        ).save()

    @classmethod
    async def get_count(cls) -> dict:
        return await cls.all()

    @classmethod
    async def get_all(cls) -> list:
        return await cls.all()

    @classmethod
    async def get_status(cls, telegram_id: int) -> Union[str, bool]:
        try:
            user = await cls.get(telegram_id=telegram_id)
            return user.status if user else False
        except DoesNotExist:
            return False
        
    @classmethod
    async def set_status(cls, telegram_id: int, status: str) -> bool:
        try:
            user = await cls.get(telegram_id=telegram_id)
            user.status = status
            await user.save()
            return True
        except DoesNotExist:
            return False

    @classmethod
    async def add_to_favourites(cls, telegram_id: int, book_id: int) -> bool:
        try:
            user = await cls.get(telegram_id=telegram_id)
            if book_id not in user.favourites:
                user.favourites.append(book_id)
                await user.save()
            return True
        except DoesNotExist:
            return False
        
    @classmethod
    async def remove_from_favourites(cls, telegram_id: int, book_id: int) -> bool:
        try:
            user = await cls.get(telegram_id=telegram_id)
            if book_id in user.favourites:
                user.favourites.remove(book_id)
                await user.save()
            return True
        except DoesNotExist:
            return False
        
    @classmethod
    async def add_to_reading_list(cls, telegram_id: int, book_id: int, page: int, chapter: int) -> bool:
        try:
            user = await cls.get(telegram_id=telegram_id)
            if book_id not in user.reading_list:
                user.reading_list.append({
                    'book_id': book_id,
                    'page': page,
                    'chapter': chapter
                })
                await user.save()
            return True
        except DoesNotExist:
            return False
        
    @classmethod
    async def remove_from_reading_list(cls, telegram_id: int, book_id: int) -> bool:
        try:
            user = await cls.get(telegram_id=telegram_id)
            if book_id in user.reading_list:
                user.reading_list.remove(book_id)
                await user.save()
            return True
        except DoesNotExist:
            return False
        
    @classmethod
    async def add_to_readed(cls, telegram_id: int, book_id: int) -> bool:
        try:
            user = await cls.get(telegram_id=telegram_id)
            if book_id not in user.readed:
                user.readed.append(book_id)
                await user.save()
            return True
        except DoesNotExist:
            return False
