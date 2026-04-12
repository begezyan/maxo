from maxo.types.base import BotMixin
from maxo.types.buttons import InlineButtons


class Keyboard(BotMixin):
    """
    Клавиатура - это двумерный массив кнопок

    Args:
        buttons:
    """

    buttons: list[list[InlineButtons]]
