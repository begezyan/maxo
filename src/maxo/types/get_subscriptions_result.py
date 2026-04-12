from maxo.types.base import BotMixin
from maxo.types.subscription import Subscription


class GetSubscriptionsResult(BotMixin):
    """
    Список всех WebHook подписок

    Args:
        subscriptions: Список текущих подписок
    """

    subscriptions: list[Subscription]
    """Список текущих подписок"""
