from typing import TYPE_CHECKING

from maxo.enums.update_type import UpdateType
from maxo.routing.updates.base import MaxUpdate
from maxo.types.user import User

if TYPE_CHECKING:
    from maxo.utils.facades import BotRemovedFromChatFacade


class BotRemovedFromChat(MaxUpdate):
    """
    Вы получите этот update, как только бот будет удалён из чата

    Args:
        chat_id: ID чата, откуда был удалён бот
        is_channel: Указывает, был ли бот удалён из канала или нет
        type:
        user: Пользователь, удаливший бота из чата
    """

    type = UpdateType.BOT_REMOVED

    chat_id: int
    """ID чата, откуда был удалён бот"""
    is_channel: bool
    """Указывает, был ли бот удалён из канала или нет"""
    user: User
    """Пользователь, удаливший бота из чата"""

    @property
    def facade(self) -> "BotRemovedFromChatFacade":
        from maxo.utils.facades import BotRemovedFromChatFacade

        return BotRemovedFromChatFacade(self.bot, self)

    if TYPE_CHECKING:
        from maxo.utils.type_promote import promote
        send_message = promote(BotRemovedFromChatFacade.send_message)
        get_chat = promote(BotRemovedFromChatFacade.get_chat)
        get_members = promote(BotRemovedFromChatFacade.get_members)
        leave_chat = promote(BotRemovedFromChatFacade.leave_chat)
        get_messages = promote(BotRemovedFromChatFacade.get_messages)
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
