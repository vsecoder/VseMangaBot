from aiogram_dialog import DialogRegistry

from . import popular_dialog


def register_dialogs(registry: DialogRegistry):
    from . import popular_dialog

    registry.register(popular_dialog.ui)
