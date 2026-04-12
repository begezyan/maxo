from maxo.types.base import BotMixin


class PhotoToken(BotMixin):
    """
    Args:
        token: Закодированная информация загруженного изображения
    """

    token: str
    """Закодированная информация загруженного изображения"""
