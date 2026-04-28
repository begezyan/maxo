from abc import abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from maxo import Bot


class BaseMethodsFacade:
    @property
    @abstractmethod
    def bot(self) -> "Bot":
        raise NotImplementedError
