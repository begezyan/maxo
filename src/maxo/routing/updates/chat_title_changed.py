from collections.abc import Awaitable, Callable
from typing import TYPE_CHECKING

from maxo.enums.update_type import UpdateType
from maxo.routing.updates.base import MaxUpdate
from maxo.types.chat import Chat
from maxo.types.chat_members_list import ChatMembersList
from maxo.types.message import Message
from maxo.types.message_list import MessageList
from maxo.types.simple_query_result import SimpleQueryResult
from maxo.types.user import User

if TYPE_CHECKING:
    from maxo.utils.facades import ChatTitleChangedFacade


class ChatTitleChanged(MaxUpdate["ChatTitleChangedFacade"]):
    """
    BБот получит это обновление, когда будет изменено название чата

    Args:
        chat_id: ID чата, где произошло событие
        title: Новое название
        type:
        user: Пользователь, который изменил название
    """

    type = UpdateType.CHAT_TITLE_CHANGED

    chat_id: int
    """ID чата, где произошло событие"""
    title: str
    """Новое название"""
    user: User
    """Пользователь, который изменил название"""

    @property
    def facade(self) -> "ChatTitleChangedFacade":
        from maxo.utils.facades import ChatTitleChangedFacade

        return ChatTitleChangedFacade(self.bot, self)

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
