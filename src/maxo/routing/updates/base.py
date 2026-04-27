from abc import abstractmethod
from datetime import datetime
from typing import TYPE_CHECKING, ClassVar, Self

from maxo.enums import UpdateType
from maxo.types.base import MaxoType

if TYPE_CHECKING:
    from maxo.utils.facades import BaseUpdateFacade


class BaseUpdate(MaxoType):
    pass


class MaxUpdate(BaseUpdate):
    """
    Базовый класс для всех апдейтов из Макса.

    У всех апдейтов есть тип (`type`, `update_type`) и время (`timestamp`).
    Фасад (`facade`) объединяет методы для работы с апдейтом,
    например, отправить сообщение или ответить на колбэк.
    """

    type: ClassVar[UpdateType]
    timestamp: datetime

    @property
    def update_type(self) -> UpdateType:
        return self.type

    @property
    @abstractmethod
    def facade(self) -> "BaseUpdateFacade[Self]":
        pass
