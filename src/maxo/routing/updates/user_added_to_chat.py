from collections.abc import Awaitable, Callable
from typing import TYPE_CHECKING

from maxo.enums.update_type import UpdateType
from maxo.errors import AttributeIsEmptyError
from maxo.omit import Omittable, Omitted, is_defined
from maxo.routing.updates.base import MaxUpdate
from maxo.types.chat import Chat
from maxo.types.chat_members_list import ChatMembersList
from maxo.types.message import Message
from maxo.types.message_list import MessageList
from maxo.types.simple_query_result import SimpleQueryResult
from maxo.types.user import User

if TYPE_CHECKING:
    from maxo.utils.facades import UserAddedToChatFacade


class UserAddedToChat(MaxUpdate["UserAddedToChatFacade"]):
    """
    Вы получите это обновление, когда пользователь будет добавлен в чат, где бот является администратором

    Args:
        chat_id: ID чата, где произошло событие
        inviter_id: Пользователь, который добавил пользователя в чат. Может быть `null`, если пользователь присоединился к чату по ссылке
        is_channel: Указывает, был ли пользователь добавлен в канал или нет
        type:
        user: Пользователь, добавленный в чат
    """

    type = UpdateType.USER_ADDED

    chat_id: int
    """ID чата, где произошло событие"""
    is_channel: bool
    """Указывает, был ли пользователь добавлен в канал или нет"""
    user: User
    """Пользователь, добавленный в чат"""

    inviter_id: Omittable[int | None] = Omitted()
    """Пользователь, который добавил пользователя в чат. Может быть `null`, если пользователь присоединился к чату по ссылке"""

    @property
    def unsafe_inviter_id(self) -> int:
        if is_defined(self.inviter_id):
            return self.inviter_id

        raise AttributeIsEmptyError(
            obj=self,
            attr="inviter_id",
        )

    @property
    def facade(self) -> "UserAddedToChatFacade":
        from maxo.utils.facades import UserAddedToChatFacade

        return UserAddedToChatFacade(self.bot, self)

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
