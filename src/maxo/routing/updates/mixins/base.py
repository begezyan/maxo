from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from maxo import Bot


class BaseMethodsFacade(ABC):
    __slots__ = ()

    @property
    @abstractmethod
    def bot(self) -> "Bot":
        raise NotImplementedError
