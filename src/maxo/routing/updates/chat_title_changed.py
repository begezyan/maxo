from typing import TYPE_CHECKING

from maxo.enums.update_type import UpdateType
from maxo.routing.updates.base import MaxUpdate
from maxo.types.user import User

if TYPE_CHECKING:
    from maxo.utils.facades import ChatTitleChangedFacade


class ChatTitleChanged(MaxUpdate):
    """
    BБот получит это обновление, когда будет изменено название чата

    Args:
        chat_id: ID чата, где произошло событие
        title: Новое название
        type:
        user: Пользователь, который изменил название
    """

    type = UpdateType.CHAT_TITLE_CHANGED

    chat_id: int
    """ID чата, где произошло событие"""
    title: str
    """Новое название"""
    user: User
    """Пользователь, который изменил название"""

    @property
    def facade(self) -> "ChatTitleChangedFacade":
        from maxo.utils.facades import ChatTitleChangedFacade

        return ChatTitleChangedFacade(self.bot, self)

    if TYPE_CHECKING:
        from maxo.utils.type_promote import promote

        send_message = promote(ChatTitleChangedFacade.send_message)
        get_chat = promote(ChatTitleChangedFacade.get_chat)
        get_members = promote(ChatTitleChangedFacade.get_members)
        leave_chat = promote(ChatTitleChangedFacade.leave_chat)
        get_messages = promote(ChatTitleChangedFacade.get_messages)
    else:

        @property
        def send_message(self):
            return self.facade.send_message

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
        def get_messages(self):
            return self.facade.get_messages
