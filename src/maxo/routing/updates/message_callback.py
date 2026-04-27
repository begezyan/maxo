from typing import TYPE_CHECKING, TypeAlias

from maxo.enums.update_type import UpdateType
from maxo.errors import AttributeIsEmptyError
from maxo.omit import Omittable, Omitted, is_defined
from maxo.routing.updates.base import MaxUpdate
from maxo.types.callback import Callback
from maxo.types.message import Message
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

    from_user = user  # Подражание aiogram

    @property
    def facade(self) -> "MessageCallbackFacade":
        from maxo.utils.facades import MessageCallbackFacade

        return MessageCallbackFacade(self.bot, self)

    if TYPE_CHECKING:
        from maxo.utils.type_promote import promote

        send_message = promote(MessageCallbackFacade.send_message)
        answer = promote(MessageCallbackFacade.answer)
        reply = promote(MessageCallbackFacade.reply)
        send_media = promote(MessageCallbackFacade.send_media)
        edit_message = promote(MessageCallbackFacade.edit_message)
        delete_message = promote(MessageCallbackFacade.delete_message)
        get_chat = promote(MessageCallbackFacade.get_chat)
        get_members = promote(MessageCallbackFacade.get_members)
        leave_chat = promote(MessageCallbackFacade.leave_chat)
        get_message_by_id = promote(MessageCallbackFacade.get_message_by_id)
        callback_answer = promote(MessageCallbackFacade.callback_answer)
    else:

        @property
        def delete_message(self):
            return self.facade.delete_message

        @property
        def send_message(self):
            return self.facade.send_message

        @property
        def answer(self):
            return self.facade.answer

        @property
        def reply(self):
            return self.facade.reply

        @property
        def send_media(self):
            return self.facade.send_media

        @property
        def edit_message(self):
            return self.facade.edit_message

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
        def get_message_by_id(self):
            return self.facade.get_message_by_id

        @property
        def callback_answer(self):
            return self.facade.callback_answer


CallbackQuery: TypeAlias = MessageCallback  # Подражание aiogram
