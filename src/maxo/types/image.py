from maxo.types.base import BotMixin


class Image(BotMixin):
    """
    Общая схема, описывающая объект изображения

    Args:
        url: URL изображения
    """

    url: str
    """URL изображения"""
