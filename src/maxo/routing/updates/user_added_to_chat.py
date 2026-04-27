from typing import TYPE_CHECKING

from maxo.enums.update_type import UpdateType
from maxo.errors import AttributeIsEmptyError
from maxo.omit import Omittable, Omitted, is_defined
from maxo.routing.updates.base import MaxUpdate
from maxo.types.user import User

if TYPE_CHECKING:
    from maxo.utils.facades import UserAddedToChatFacade


class UserAddedToChat(MaxUpdate):
    """
    Вы получите это обновление, когда пользователь будет добавлен в чат, где бот является администратором

    Args:
        chat_id: ID чата, где произошло событие
        inviter_id: Пользователь, который добавил пользователя в чат. Может быть `null`, если пользователь присоединился к чату по ссылке
        is_channel: Указывает, был ли пользователь добавлен в канал или нет
        type:
        user: Пользователь, добавленный в чат
    """

    type = UpdateType.USER_ADDED

    chat_id: int
    """ID чата, где произошло событие"""
    is_channel: bool
    """Указывает, был ли пользователь добавлен в канал или нет"""
    user: User
    """Пользователь, добавленный в чат"""

    inviter_id: Omittable[int | None] = Omitted()
    """Пользователь, который добавил пользователя в чат. Может быть `null`, если пользователь присоединился к чату по ссылке"""

    @property
    def unsafe_inviter_id(self) -> int:
        if is_defined(self.inviter_id):
            return self.inviter_id

        raise AttributeIsEmptyError(
            obj=self,
            attr="inviter_id",
        )

    @property
    def facade(self) -> "UserAddedToChatFacade":
        from maxo.utils.facades import UserAddedToChatFacade

        return UserAddedToChatFacade(self.bot, self)

    if TYPE_CHECKING:
        from maxo.utils.type_promote import promote

        send_message = promote(UserAddedToChatFacade.send_message)
        get_chat = promote(UserAddedToChatFacade.get_chat)
        get_members = promote(UserAddedToChatFacade.get_members)
        leave_chat = promote(UserAddedToChatFacade.leave_chat)
        get_messages = promote(UserAddedToChatFacade.get_messages)
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
