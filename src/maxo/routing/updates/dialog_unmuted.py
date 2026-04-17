from typing import TYPE_CHECKING

from maxo.enums.update_type import UpdateType
from maxo.errors import AttributeIsEmptyError
from maxo.omit import Omittable, Omitted, is_defined
from maxo.routing.updates.base import MaxUpdate
from maxo.types.user import User

if TYPE_CHECKING:
    from maxo.utils.facades import DialogUnmutedFacade


class DialogUnmuted(MaxUpdate):
    """
    Вы получите этот update, когда пользователь включит уведомления в диалоге с ботом

    Args:
        chat_id: ID чата, где произошло событие
        type:
        user: Пользователь, который включил уведомления
        user_locale: Текущий язык пользователя в формате IETF BCP 47
    """

    type = UpdateType.DIALOG_UNMUTED

    chat_id: int
    """ID чата, где произошло событие"""
    user: User
    """Пользователь, который включил уведомления"""

    user_locale: Omittable[str] = Omitted()
    """Текущий язык пользователя в формате IETF BCP 47"""

    @property
    def unsafe_user_locale(self) -> str:
        if is_defined(self.user_locale):
            return self.user_locale

        raise AttributeIsEmptyError(
            obj=self,
            attr="user_locale",
        )

    @property
    def facade(self) -> "DialogUnmutedFacade":
        from maxo.utils.facades import DialogUnmutedFacade

        return DialogUnmutedFacade(self.bot, self)
    if TYPE_CHECKING:
        from maxo.utils.type_promote import promote
        send_message = promote(DialogUnmutedFacade.send_message)
        get_chat = promote(DialogUnmutedFacade.get_chat)
        get_members = promote(DialogUnmutedFacade.get_members)
        leave_chat = promote(DialogUnmutedFacade.leave_chat)
        get_messages = promote(DialogUnmutedFacade.get_messages)
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
