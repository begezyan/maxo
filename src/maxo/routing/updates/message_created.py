from collections.abc import Awaitable, Callable
from typing import TYPE_CHECKING

from maxo.enums.update_type import UpdateType
from maxo.errors import AttributeIsEmptyError
from maxo.omit import Omittable, Omitted, is_defined
from maxo.routing.updates.base import MaxUpdate
from maxo.types.chat import Chat
from maxo.types.chat_members_list import ChatMembersList
from maxo.types.message import Message
from maxo.types.simple_query_result import SimpleQueryResult

if TYPE_CHECKING:
    from maxo.utils.facades import MessageCreatedFacade


class MessageCreated(MaxUpdate["MessageCreatedFacade"]):
    """
    ы получите этот `update`, как только сообщение будет создано

    Args:
        message: Новое созданное сообщение
        type:
        user_locale: Текущий язык пользователя в формате IETF BCP 47. Доступно только в диалогах
    """

    type = UpdateType.MESSAGE_CREATED

    message: Message
    """Новое созданное сообщение"""

    user_locale: Omittable[str | None] = Omitted()
    """Текущий язык пользователя в формате IETF BCP 47. Доступно только в диалогах"""

    @property
    def unsafe_user_locale(self) -> str:
        if is_defined(self.user_locale):
            return self.user_locale

        raise AttributeIsEmptyError(
            obj=self,
            attr="user_locale",
        )

    @property
    def text(self) -> str | None:
        return self.message.body.text

    @property
    def facade(self) -> "MessageCreatedFacade":
        from maxo.utils.facades import MessageCreatedFacade

        return MessageCreatedFacade(self.bot, self)

    @property
    def send_message(self) -> Callable[..., Awaitable[Message]]:
        return self.facade.send_message

    @property
    def answer(self) -> Callable[..., Awaitable[Message]]:
        return self.facade.answer

    @property
    def reply(self) -> Callable[..., Awaitable[Message]]:
        return self.facade.reply

    @property
    def send_media(self) -> Callable[..., Awaitable[Message]]:
        return self.facade.send_media

    @property
    def edit_message(self) -> Callable[..., Awaitable[Message]]:
        return self.facade.edit_message

    @property
    def delete_message(self) -> Callable[..., Awaitable["SimpleQueryResult"]]:
        return self.facade.delete_message

    @property
    def get_chat(self) -> Callable[..., Awaitable["Chat"]]:
        return self.facade.get_chat

    @property
    def get_members(self) -> Callable[..., Awaitable["ChatMembersList"]]:
        return self.facade.get_members

    @property
    def leave_chat(self) -> Callable[..., Awaitable["SimpleQueryResult"]]:
        return self.facade.leave_chat

    @property
    def get_message_by_id(self) -> Callable[..., Awaitable[Message]]:
        return self.facade.get_message_by_id
