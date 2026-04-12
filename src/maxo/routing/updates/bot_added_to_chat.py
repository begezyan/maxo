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
    from maxo.utils.facades import BotAddedToChatFacade


class BotAddedToChat(MaxUpdate):
    """
    Вы получите этот update, как только бот будет добавлен в чат

    Args:
        chat_id: ID чата, куда был добавлен бот
        is_channel: Указывает, был ли бот добавлен в канал или нет
        type:
        user: Пользователь, добавивший бота в чат
    """

    type = UpdateType.BOT_ADDED

    chat_id: int
    """ID чата, куда был добавлен бот"""
    is_channel: bool
    """Указывает, был ли бот добавлен в канал или нет"""
    user: User
    """Пользователь, добавивший бота в чат"""

    @property
    def facade(self) -> "BotAddedToChatFacade":
        from maxo.utils.facades import BotAddedToChatFacade

        return BotAddedToChatFacade(self.bot, self)

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
