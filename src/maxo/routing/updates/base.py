from datetime import datetime
from typing import ClassVar

from maxo.enums import UpdateType
from maxo.types.base import BotMixin


class BaseUpdate(BotMixin):
    pass


class MaxUpdate(BaseUpdate):
    type: ClassVar[UpdateType]
    timestamp: datetime

    @property
    def update_type(self) -> UpdateType:
        return self.type
