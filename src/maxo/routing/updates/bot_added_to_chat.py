from maxo.enums.update_type import UpdateType
from maxo.routing.updates.base import MaxUpdate
from maxo.routing.updates.mixins import ChatMethodsFacade
from maxo.types.user import User


class BotAddedToChat(MaxUpdate, ChatMethodsFacade):
    """
    Вы получите это событие, как только бот будет добавлен в чат или канал

    Args:
        chat_id: ID чата, куда был добавлен бот
        is_channel: Указывает, что бот добавлен в канал, а не в чат
        type:
        user: Пользователь, добавивший бота в чат
    """

    type = UpdateType.BOT_ADDED

    chat_id: int
    """ID чата, куда был добавлен бот"""
    is_channel: bool
    """Указывает, что бот добавлен в канал, а не в чат"""
    user: User
    """Пользователь, добавивший бота в чат"""
