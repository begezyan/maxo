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
    from maxo.utils.facades import DialogRemovedFacade


class DialogRemoved(MaxUpdate["DialogRemovedFacade"]):
    """
    Вы получите этот update, когда пользователь удаляет чат

    Args:
        chat_id: ID чата, где произошло событие
        type:
        user: Пользователь, который удалил чат
        user_locale: Текущий язык пользователя в формате IETF BCP 47
    """

    type = UpdateType.DIALOG_REMOVED

    chat_id: int
    """ID чата, где произошло событие"""
    user: User
    """Пользователь, который удалил чат"""

    user_locale: Omittable[str] = Omitted()
    """Текущий язык пользователя в формате IETF BCP 47"""

    @property
    def unsafe_user_locale(self) -> str:
        if is_defined(self.user_locale):
            return self.user_locale

        raise AttributeIsEmptyError(
            obj=self,
            attr="user_locale",
        )

    @property
    def facade(self) -> "DialogRemovedFacade":
        from maxo.utils.facades import DialogRemovedFacade

        return DialogRemovedFacade(self.bot, self)

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
