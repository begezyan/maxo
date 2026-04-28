from typing import TYPE_CHECKING

from maxo.enums.update_type import UpdateType
from maxo.routing.updates.base import MaxUpdate
from maxo.routing.updates.mixins import ChatMethodsFacade

if TYPE_CHECKING:
    from maxo.routing.facades import MessageRemovedFacade


class MessageRemoved(MaxUpdate, ChatMethodsFacade):
    """
    Вы получите этот `update`, как только сообщение будет удалено

    Args:
        chat_id: ID чата, где сообщение было удалено
        message_id: ID удаленного сообщения
        type:
        user_id: Пользователь, удаливший сообщение
    """

    type = UpdateType.MESSAGE_REMOVED

    chat_id: int
    """ID чата, где сообщение было удалено"""
    message_id: str
    """ID удаленного сообщения"""
    user_id: int
    """Пользователь, удаливший сообщение"""

    @property
    def facade(self) -> "MessageRemovedFacade":
        from maxo.routing.facades import MessageRemovedFacade

        return MessageRemovedFacade(self.bot, self)
