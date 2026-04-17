from typing import TYPE_CHECKING

from maxo.enums.update_type import UpdateType
from maxo.routing.updates.base import MaxUpdate
from maxo.types.message import Message

if TYPE_CHECKING:
    from maxo.utils.facades import MessageEditedFacade


class MessageEdited(MaxUpdate):
    """
    Вы получите этот `update`, как только сообщение будет отредактировано

    Args:
        message: Отредактированное сообщение
        type:
    """

    type = UpdateType.MESSAGE_EDITED

    message: Message
    """Отредактированное сообщение"""

    @property
    def text(self) -> str | None:
        return self.message.body.text

    @property
    def facade(self) -> "MessageEditedFacade":
        from maxo.utils.facades import MessageEditedFacade

        return MessageEditedFacade(self.bot, self)
    if TYPE_CHECKING:
        from maxo.utils.type_promote import promote
        send_message = promote(MessageEditedFacade.send_message)
        answer = promote(MessageEditedFacade.answer)
        reply = promote(MessageEditedFacade.reply)
        send_media = promote(MessageEditedFacade.send_media)
        edit_message = promote(MessageEditedFacade.edit_message)
        delete_message = promote(MessageEditedFacade.delete_message)
        get_chat = promote(MessageEditedFacade.get_chat)
        get_members = promote(MessageEditedFacade.get_members)
        leave_chat = promote(MessageEditedFacade.leave_chat)
        get_message_by_id = promote(MessageEditedFacade.get_message_by_id)
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
