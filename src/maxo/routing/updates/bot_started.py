from typing import TYPE_CHECKING

from maxo.enums.update_type import UpdateType
from maxo.errors import AttributeIsEmptyError
from maxo.omit import Omittable, Omitted, is_defined
from maxo.routing.updates.base import MaxUpdate
from maxo.types.user import User

if TYPE_CHECKING:
    from maxo.utils.facades import BotStartedFacade


class BotStarted(MaxUpdate):
    """
    Бот получает этот тип обновления, как только пользователь нажал кнопку `Start`

    Args:
        chat_id: ID диалога, где произошло событие
        payload: Дополнительные данные из дип-линков, переданные при запуске бота
        type:
        user: Пользователь, который нажал кнопку 'Start'
        user_locale: Текущий язык пользователя в формате IETF BCP 47
    """

    type = UpdateType.BOT_STARTED

    chat_id: int
    """ID диалога, где произошло событие"""
    user: User
    """Пользователь, который нажал кнопку 'Start'"""

    payload: Omittable[str | None] = Omitted()
    """Дополнительные данные из дип-линков, переданные при запуске бота"""
    user_locale: Omittable[str] = Omitted()
    """Текущий язык пользователя в формате IETF BCP 47"""

    @property
    def unsafe_payload(self) -> str:
        if is_defined(self.payload):
            return self.payload

        raise AttributeIsEmptyError(
            obj=self,
            attr="payload",
        )

    @property
    def unsafe_user_locale(self) -> str:
        if is_defined(self.user_locale):
            return self.user_locale

        raise AttributeIsEmptyError(
            obj=self,
            attr="user_locale",
        )

    @property
    def facade(self) -> "BotStartedFacade":
        from maxo.utils.facades import BotStartedFacade

        return BotStartedFacade(self.bot, self)

    if TYPE_CHECKING:
        from maxo.utils.type_promote import promote

        send_message = promote(BotStartedFacade.send_message)
        get_chat = promote(BotStartedFacade.get_chat)
        get_members = promote(BotStartedFacade.get_members)
        leave_chat = promote(BotStartedFacade.leave_chat)
        get_messages = promote(BotStartedFacade.get_messages)
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
