from typing import TYPE_CHECKING

from maxo.enums.update_type import UpdateType
from maxo.routing.updates.base import MaxUpdate

if TYPE_CHECKING:

    from maxo.utils.facades import MessageRemovedFacade


class MessageRemoved(MaxUpdate):
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
        from maxo.utils.facades import MessageRemovedFacade

        return MessageRemovedFacade(self.bot, self)
    if TYPE_CHECKING:
        from maxo.utils.type_promote import promote
        send_message = promote(MessageRemovedFacade.send_message)
        get_chat = promote(MessageRemovedFacade.get_chat)
        get_members = promote(MessageRemovedFacade.get_members)
        leave_chat = promote(MessageRemovedFacade.leave_chat)
        get_messages = promote(MessageRemovedFacade.get_messages)
    else:
        @property
        def send_message(self):
            return self.facade.send_message

        @property
        def get_chat(self):
            return self.facade.get_chat

        @property
        def get_members(self):
            return self.facade.get_members

        @property
        def leave_chat(self):
            return self.facade.leave_chat

        @property
        def get_messages(self):
            return self.facade.get_messages
