from maxo.enums import AttachmentType
from maxo.types.attachment import Attachment


class DataAttachment(Attachment):
    """Attachment contains payload sent through `SendMessageButton`"""

    type: AttachmentType = AttachmentType.DATA

    data: str
