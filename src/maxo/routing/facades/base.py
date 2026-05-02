from typing import Generic, TypeVar

from maxo.bot.bot import Bot
from maxo.routing.updates.base import BaseUpdate
from maxo.routing.updates.mixins.subscription import SubscriptionMethodsFacade

_UpdateT = TypeVar("_UpdateT", bound=BaseUpdate)


class BaseUpdateFacade(SubscriptionMethodsFacade, Generic[_UpdateT]):
    def __init__(
        self,
        bot: Bot,
        update: _UpdateT,
    ) -> None:
        self._bot = bot
        self._update = update

    @property
    def update(self) -> _UpdateT:
        return self._update

    @property
    def bot(self) -> Bot:
        return self._bot
