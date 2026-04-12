from maxo.types.base import BotMixin
from maxo.types.buttons import InlineButtons


class InlineKeyboardAttachmentRequestPayload(BotMixin):
    """
    Args:
        buttons: Двумерный массив кнопок
    """

    buttons: list[list[InlineButtons]]
    """Двумерный массив кнопок"""
