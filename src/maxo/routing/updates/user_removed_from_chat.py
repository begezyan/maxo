from typing import TYPE_CHECKING

from maxo.enums.update_type import UpdateType
from maxo.errors import AttributeIsEmptyError
from maxo.omit import Omittable, Omitted, is_defined
from maxo.routing.updates.base import MaxUpdate
from maxo.types.user import User

if TYPE_CHECKING:
    from maxo.utils.facades import UserRemovedFromChatFacade


class UserRemovedFromChat(MaxUpdate):
    """
    Вы получите это обновление, когда пользователь будет удалён из чата, где бот является администратором

    Args:
        admin_id: Администратор, который удалил пользователя из чата. Может быть `null`, если пользователь покинул чат сам
        chat_id: ID чата, где произошло событие
        is_channel: Указывает, был ли пользователь удалён из канала или нет
        type:
        user: Пользователь, удалённый из чата
    """

    type = UpdateType.USER_REMOVED

    chat_id: int
    """ID чата, где произошло событие"""
    is_channel: bool
    """Указывает, был ли пользователь удалён из канала или нет"""
    user: User
    """Пользователь, удалённый из чата"""

    admin_id: Omittable[int] = Omitted()
    """Администратор, который удалил пользователя из чата. Может быть `null`, если пользователь покинул чат сам"""

    @property
    def unsafe_admin_id(self) -> int:
        if is_defined(self.admin_id):
            return self.admin_id

        raise AttributeIsEmptyError(
            obj=self,
            attr="admin_id",
        )

    @property
    def facade(self) -> "UserRemovedFromChatFacade":
        from maxo.utils.facades import UserRemovedFromChatFacade

        return UserRemovedFromChatFacade(self.bot, self)

    if TYPE_CHECKING:
        from maxo.utils.type_promote import promote

        send_message = promote(UserRemovedFromChatFacade.send_message)
        get_chat = promote(UserRemovedFromChatFacade.get_chat)
        get_members = promote(UserRemovedFromChatFacade.get_members)
        leave_chat = promote(UserRemovedFromChatFacade.leave_chat)
        get_messages = promote(UserRemovedFromChatFacade.get_messages)
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
