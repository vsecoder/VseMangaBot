from tortoise import fields
from tortoise.models import Model


class User(Model):
    """
    DB model for users.

    Fields:
        id: int
        telegram_id: int
        name: str
        favourites: dict
        reading_list: dict
        readed: dict
        status: str
    """

    id = fields.IntField(pk=True)
    telegram_id = fields.IntField(unique=True)
    name = fields.CharField(max_length=255)
    favourites = fields.JSONField(default=[])
    reading_list = fields.JSONField(default=[])
    readed = fields.JSONField(default=[])
    status = fields.CharField(max_length=255, default="user")
