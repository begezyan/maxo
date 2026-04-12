from maxo.types.base import BotMixin


class StickerAttachmentRequestPayload(BotMixin):
    """
    Args:
        code: Код стикера
    """

    code: str
    """Код стикера"""
