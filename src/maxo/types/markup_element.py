from maxo.enums import MarkupElementType
from maxo.types.base import MaxoType


class MarkupElement(MaxoType):
    from_: int
    length: int
    type: MarkupElementType
