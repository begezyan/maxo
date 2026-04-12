from collections.abc import Awaitable, Callable
from typing import TYPE_CHECKING, TypeAlias

from maxo.enums.update_type import UpdateType
from maxo.errors import AttributeIsEmptyError
from maxo.omit import Omittable, Omitted, is_defined
from maxo.routing.updates.base import MaxUpdate
from maxo.types.callback import Callback
from maxo.types.chat import Chat
from maxo.types.chat_members_list import ChatMembersList
from maxo.types.message import Message
from maxo.types.simple_query_result import SimpleQueryResult
from maxo.types.user import User

if TYPE_CHECKING:
    from maxo.utils.facades import MessageCallbackFacade


class MessageCallback(MaxUpdate):
    """
    Вы получите этот `update` как только пользователь нажмёт кнопку

    Args:
        callback:
        message: Изначальное сообщение, содержащее встроенную клавиатуру. Может быть `null`, если оно было удалено к моменту, когда бот получил это обновление
        type:
        user_locale: Текущий язык пользователя в формате IETF BCP 47
    """

    type = UpdateType.MESSAGE_CALLBACK

    callback: Callback

    message: Message | None = None
    """Изначальное сообщение, содержащее встроенную клавиатуру. Может быть `null`, если оно было удалено к моменту, когда бот получил это обновление"""

    user_locale: Omittable[str | None] = Omitted()
    """Текущий язык пользователя в формате IETF BCP 47"""

    @property
    def unsafe_message(self) -> Message:
        if is_defined(self.message):
            return self.message

        raise AttributeIsEmptyError(
            obj=self,
            attr="message",
        )

    @property
    def unsafe_user_locale(self) -> str:
        if is_defined(self.user_locale):
            return self.user_locale

        raise AttributeIsEmptyError(
            obj=self,
            attr="user_locale",
        )

    @property
    def callback_id(self) -> str:
        return self.callback.callback_id

    @property
    def payload(self) -> str | None:
        return self.callback.payload

    @property
    def user(self) -> User:
        return self.callback.user

    @property
    def facade(self) -> "MessageCallbackFacade":
        from maxo.utils.facades import MessageCallbackFacade

        return MessageCallbackFacade(self.bot, self)

    @property
    def delete_message(self) -> Callable[..., Awaitable[SimpleQueryResult]]:
        return self.facade.delete_message

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
    def get_chat(self) -> Callable[..., Awaitable[Chat]]:
        return self.facade.get_chat

    @property
    def get_members(self) -> Callable[..., Awaitable[ChatMembersList]]:
        return self.facade.get_members

    @property
    def leave_chat(self) -> Callable[..., Awaitable[SimpleQueryResult]]:
        return self.facade.leave_chat

    @property
    def get_message_by_id(self) -> Callable[..., Awaitable[Message]]:
        return self.facade.get_message_by_id

    @property
    def callback_answer(self) -> Callable[..., Awaitable[SimpleQueryResult]]:
        return self.facade.callback_answer


CallbackQuery: TypeAlias = MessageCallback  # Подражание aiogram
