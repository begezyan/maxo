from datetime import datetime

from maxo.types.base import MaxoType
from maxo.types.user import User


class Callback(MaxoType):
    timestamp: datetime
    callback_id: str
    payload: str | None = None
    user: User

    @property
    def id(self) -> str:
        return self.callback_id
