from typing import Any

from maxo.bot.methods.base import MaxoMethod
from maxo.bot.methods.markers import Query
from maxo.omit import Omittable, Omitted
from maxo.types.message_list import MessageList


class GetMessages(MaxoMethod[MessageList]):
    """Получение сообщений."""

    __url__ = "messages"
    __method__ = "get"

    chat_id: Query[Omittable[int]] = Omitted()
    count: Query[Omittable[int]] = Omitted()
    from_: Query[Omittable[int]] = Omitted()
    message_ids: Query[Omittable[Any | None]] = Omitted()
    to: Query[Omittable[int]] = Omitted()
