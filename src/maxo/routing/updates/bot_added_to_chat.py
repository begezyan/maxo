from typing import TYPE_CHECKING

from maxo.enums.update_type import UpdateType
from maxo.routing.updates.base import MaxUpdate
from maxo.types.user import User

if TYPE_CHECKING:
    from maxo.utils.facades import BotAddedToChatFacade


class BotAddedToChat(MaxUpdate):
    """
    Вы получите этот update, как только бот будет добавлен в чат

    Args:
        chat_id: ID чата, куда был добавлен бот
        is_channel: Указывает, был ли бот добавлен в канал или нет
        type:
        user: Пользователь, добавивший бота в чат
    """

    type = UpdateType.BOT_ADDED

    chat_id: int
    """ID чата, куда был добавлен бот"""
    is_channel: bool
    """Указывает, был ли бот добавлен в канал или нет"""
    user: User
    """Пользователь, добавивший бота в чат"""

    @property
    def facade(self) -> "BotAddedToChatFacade":
        from maxo.utils.facades import BotAddedToChatFacade

        return BotAddedToChatFacade(self.bot, self)

    if TYPE_CHECKING:
        from maxo.utils.type_promote import promote

        send_message = promote(BotAddedToChatFacade.send_message)
        get_chat = promote(BotAddedToChatFacade.get_chat)
        get_members = promote(BotAddedToChatFacade.get_members)
        leave_chat = promote(BotAddedToChatFacade.leave_chat)
        get_messages = promote(BotAddedToChatFacade.get_messages)
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
