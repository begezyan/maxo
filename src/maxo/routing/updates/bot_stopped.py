from typing import TYPE_CHECKING

from maxo.enums.update_type import UpdateType
from maxo.errors import AttributeIsEmptyError
from maxo.omit import Omittable, Omitted, is_defined
from maxo.routing.updates.base import MaxUpdate
from maxo.types.user import User

if TYPE_CHECKING:
    from maxo.utils.facades import BotStoppedFacade


class BotStopped(MaxUpdate):
    """
    Бот получает этот тип обновления, как только пользователь останавливает бота

    Args:
        chat_id: ID диалога, где произошло событие
        type:
        user: Пользователь, который остановил чат
        user_locale: Текущий язык пользователя в формате IETF BCP 47
    """

    type = UpdateType.BOT_STOPPED

    chat_id: int
    """ID диалога, где произошло событие"""
    user: User
    """Пользователь, который остановил чат"""

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
    def facade(self) -> "BotStoppedFacade":
        from maxo.utils.facades import BotStoppedFacade

        return BotStoppedFacade(self.bot, self)
    if TYPE_CHECKING:
        from maxo.utils.type_promote import promote
        send_message = promote(BotStoppedFacade.send_message)
        get_chat = promote(BotStoppedFacade.get_chat)
        get_members = promote(BotStoppedFacade.get_members)
        leave_chat = promote(BotStoppedFacade.leave_chat)
        get_messages = promote(BotStoppedFacade.get_messages)
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
