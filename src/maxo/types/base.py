from abc import ABCMeta
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Optional, Self, dataclass_transform

from maxo.errors import AttributeIsEmptyError
from maxo.omit import is_defined

if TYPE_CHECKING:
    from maxo import Bot


@dataclass_transform(
    frozen_default=False,
    kw_only_default=True,
)
class _MaxoTypeMetaClass(type):
    def __new__(
        cls,
        name: str,
        bases: tuple[Any, ...],
        namespace: dict[str, Any],
        slots: bool = True,
        **kwargs: Any,
    ) -> Any:
        class_ = super().__new__(cls, name, bases, namespace, **kwargs)
        if "__slots__" in namespace:
            return class_

        return dataclass(
            slots=slots,
            frozen=False,
            kw_only=True,
        )(class_)


class _MaxoTypeABCMeta(_MaxoTypeMetaClass, ABCMeta):
    pass


class BaseMaxoType(metaclass=_MaxoTypeABCMeta):
    pass


class BotMixin:
    __slots__ = ("_bot",)

    @property
    def bot(self) -> "Bot":
        self._bot = getattr(self, "_bot", None)

        if is_defined(self._bot):
            return self._bot

        raise AttributeIsEmptyError(
            obj=self,
            attr="_bot",
        )

    @bot.setter
    def bot(self, bot: Optional["Bot"]) -> None:
        self._bot = bot

    def as_(self, bot: Optional["Bot"]) -> Self:
        self.bot = bot
        return self


class MaxoType(BaseMaxoType, BotMixin):
    pass
