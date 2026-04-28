from abc import abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from maxo import Bot


class BaseMethodsFacade:
    """
    Класс должен наследоваться от `ABC` или `Protocol` для работы `@abstractmethod`,
    но так как `MaxoType` сделан через метакласс,
    то он конфликтует с ABC в моделях апдейтах (миксины всё такое).
    Из-за этого фасады и их наследники не наследуются от `ABC`.

    https://github.com/K1rL3s/maxo/pull/103
    https://github.com/K1rL3s/maxo/pull/107
    """

    @property
    @abstractmethod
    def bot(self) -> "Bot":
        raise NotImplementedError
