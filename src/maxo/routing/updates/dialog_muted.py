from datetime import datetime
from typing import TYPE_CHECKING

from maxo.enums.update_type import UpdateType
from maxo.errors import AttributeIsEmptyError
from maxo.omit import Omittable, Omitted, is_defined
from maxo.routing.updates.base import MaxUpdate
from maxo.types.user import User

if TYPE_CHECKING:
    from maxo.utils.facades import DialogMutedFacade


class DialogMuted(MaxUpdate):
    """
    Вы получите этот update, когда пользователь заглушит диалог с ботом

    Args:
        chat_id: ID чата, где произошло событие
        muted_until: Время в формате Unix, до наступления которого диалог был отключён
        type:
        user: Пользователь, который отключил уведомления
        user_locale: Текущий язык пользователя в формате IETF BCP 47
    """

    type = UpdateType.DIALOG_MUTED

    chat_id: int
    """ID чата, где произошло событие"""
    muted_until: datetime
    """Время в формате Unix, до наступления которого диалог был отключён"""
    user: User
    """Пользователь, который отключил уведомления"""

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
    def facade(self) -> "DialogMutedFacade":
        from maxo.utils.facades import DialogMutedFacade

        return DialogMutedFacade(self.bot, self)

    if TYPE_CHECKING:
        from maxo.utils.type_promote import promote

        send_message = promote(DialogMutedFacade.send_message)
        get_chat = promote(DialogMutedFacade.get_chat)
        get_members = promote(DialogMutedFacade.get_members)
        leave_chat = promote(DialogMutedFacade.leave_chat)
        get_messages = promote(DialogMutedFacade.get_messages)
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
