from maxo.enums.attachment_request_type import AttachmentRequestType
from maxo.types.base import BotMixin


class AttachmentRequest(BotMixin):
    """
    Запрос на прикрепление данных к сообщению

    Args:
        type:
    """

    type: AttachmentRequestType
