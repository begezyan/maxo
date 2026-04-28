from typing import TYPE_CHECKING

from maxo.enums.update_type import UpdateType
from maxo.routing.updates.base import MaxUpdate
from maxo.routing.updates.mixins.chat import ChatMethodsFacade
from maxo.types.user import User

if TYPE_CHECKING:
    from maxo.routing.facades import BotAddedToChatFacade


class BotAddedToChat(MaxUpdate, ChatMethodsFacade):
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
        from maxo.routing.facades import BotAddedToChatFacade

        return BotAddedToChatFacade(self.bot, self)
