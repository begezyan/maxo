from maxo.omit import Omittable
from maxo.routing.facades.base import BaseUpdateFacade
from maxo.routing.updates.message_created import MessageCreated
from maxo.routing.updates.mixins.message import MessageMethodsFacade
from maxo.types.message import Message


class MessageCreatedFacade(BaseUpdateFacade[MessageCreated], MessageMethodsFacade):
    __slots__ = ()

    @property
    def message(self) -> Message:
        return self._update.message

    @property
    def text(self) -> str | None:
        return self._update.text

    @property
    def user_locale(self) -> Omittable[str | None]:
        return self._update.user_locale
