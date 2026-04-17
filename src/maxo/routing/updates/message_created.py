from typing import TYPE_CHECKING

from maxo.enums.update_type import UpdateType
from maxo.errors import AttributeIsEmptyError
from maxo.omit import Omittable, Omitted, is_defined
from maxo.routing.updates.base import MaxUpdate
from maxo.types.message import Message

if TYPE_CHECKING:
    from maxo.utils.facades import MessageCreatedFacade



class MessageCreated(MaxUpdate):
    """
    Вы получите этот `update`, как только сообщение будет создано

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
    if TYPE_CHECKING:
        from maxo.utils.type_promote import promote
        send_message = promote(MessageCreatedFacade.send_message)
        answer = promote(MessageCreatedFacade.answer)
        reply = promote(MessageCreatedFacade.reply)
        send_media = promote(MessageCreatedFacade.send_media)
        edit_message = promote(MessageCreatedFacade.edit_message)
        delete_message = promote(MessageCreatedFacade.delete_message)
        get_chat = promote(MessageCreatedFacade.get_chat)
        get_members = promote(MessageCreatedFacade.get_members)
        leave_chat = promote(MessageCreatedFacade.leave_chat)
        get_message_by_id = promote(MessageCreatedFacade.get_message_by_id)
    else:
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
        def delete_message(self):
            return self.facade.delete_message

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
