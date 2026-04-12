from typing import TYPE_CHECKING

from maxo.enums.update_type import UpdateType
from maxo.routing.updates.base import MaxUpdate
from maxo.types.message import Message

if TYPE_CHECKING:
    from maxo.utils.facades import MessageEditedFacade


class MessageEdited(MaxUpdate):
    """
    Вы получите этот `update`, как только сообщение будет отредактировано

    Args:
        message: Отредактированное сообщение
        type:
    """

    type = UpdateType.MESSAGE_EDITED

    message: Message
    """Отредактированное сообщение"""

    @property
    def text(self) -> str | None:
        return self.message.body.text

    @property
    def facade(self) -> "MessageEditedFacade":
        from maxo.utils.facades import MessageEditedFacade

        return MessageEditedFacade(self.bot, self)
