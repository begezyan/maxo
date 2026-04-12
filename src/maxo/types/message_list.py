from maxo.types.base import BotMixin
from maxo.types.message import Message


class MessageList(BotMixin):
    """
    Пагинированный список сообщений

    Args:
        messages: Массив сообщений
    """

    messages: list[Message]
    """Массив сообщений"""
