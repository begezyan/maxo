from collections.abc import Awaitable, Callable
from typing import TYPE_CHECKING

from maxo.enums.update_type import UpdateType
from maxo.routing.updates.base import MaxUpdate
from maxo.types.chat import Chat
from maxo.types.chat_members_list import ChatMembersList
from maxo.types.message import Message
from maxo.types.message_list import MessageList
from maxo.types.simple_query_result import SimpleQueryResult

if TYPE_CHECKING:

    from maxo.utils.facades import MessageRemovedFacade


class MessageRemoved(MaxUpdate["MessageRemovedFacade"]):
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

    @property
    def send_message(self) -> Callable[..., Awaitable[Message]]:
        return self.facade.send_message

    @property
    def get_chat(self) -> Callable[..., Awaitable[Chat]]:
        return self.facade.get_chat

    @property
    def get_members(self) -> Callable[..., Awaitable[ChatMembersList]]:
        return self.facade.get_members

    @property
    def leave_chat(self) -> Callable[..., Awaitable[SimpleQueryResult]]:
        return self.facade.leave_chat

    @property
    def get_messages(self) -> Callable[..., Awaitable[MessageList]]:
        return self.facade.get_messages
