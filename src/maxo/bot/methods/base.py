from unihttp.method import BaseMethod

from maxo.types.base import BotMixin


class MaxoMethod[MethodResultT](BaseMethod[MethodResultT], BotMixin):
    """
    Базовый метод для методов Bot API Max.
    """
