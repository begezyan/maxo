from collections.abc import Awaitable, Callable
from typing import TYPE_CHECKING

from maxo.enums.update_type import UpdateType
from maxo.routing.updates.base import MaxUpdate
from maxo.types.chat import Chat
from maxo.types.chat_members_list import ChatMembersList
from maxo.types.message import Message
from maxo.types.simple_query_result import SimpleQueryResult

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
