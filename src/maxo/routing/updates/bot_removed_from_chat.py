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
    from maxo.utils.facades import BotRemovedFromChatFacade


class BotRemovedFromChat(MaxUpdate):
    """
    Вы получите этот update, как только бот будет удалён из чата

    Args:
        chat_id: ID чата, откуда был удалён бот
        is_channel: Указывает, был ли бот удалён из канала или нет
        type:
        user: Пользователь, удаливший бота из чата
    """

    type = UpdateType.BOT_REMOVED

    chat_id: int
    """ID чата, откуда был удалён бот"""
    is_channel: bool
    """Указывает, был ли бот удалён из канала или нет"""
    user: User
    """Пользователь, удаливший бота из чата"""

    @property
    def facade(self) -> "BotRemovedFromChatFacade":
        from maxo.utils.facades import BotRemovedFromChatFacade

        return BotRemovedFromChatFacade(self.bot, self)

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
