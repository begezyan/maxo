from maxo.types.base import BotMixin


class PhotoAttachmentPayload(BotMixin):
    """
    Args:
        photo_id: Уникальный ID этого изображения
        token:
        url: URL изображения
    """

    photo_id: int
    """Уникальный ID этого изображения"""
    token: str
    url: str
    """URL изображения"""
