from abc import abstractmethod
from typing import Protocol

from maxo import Ctx
from maxo.dialogs.api.entities import ChatEvent
from maxo.dialogs.api.protocols import (
    DialogManager,
    DialogRegistryProtocol,
)
from maxo.routing.interfaces import BaseRouter


class DialogManagerFactory(Protocol):
    @abstractmethod
    def __call__(
        self,
        event: ChatEvent,
        ctx: Ctx,
        registry: DialogRegistryProtocol,
        router: BaseRouter,
    ) -> DialogManager:
        raise NotImplementedError
