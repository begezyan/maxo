from maxo.types.base import BotMixin
from maxo.types.message import Message


class SendMessageResult(BotMixin):
    """
    Args:
        message:
    """

    message: Message
