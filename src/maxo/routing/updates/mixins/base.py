"""
Из-за того, что в BotMixin надо указать __slots__, и без __init__ это не сделать,
и наследование от BaseMethodsFacade и BotMixin одновременно ломает что-то питоновское,
и BaseMethodsFacade по сути определял только пропертю bot,
то BaseMethodsFacade просто стал BotMixin'ом.

https://github.com/K1rL3s/maxo/pull/103
https://github.com/K1rL3s/maxo/pull/107
"""

from maxo.types import BotMixin

BaseMethodsFacade = BotMixin
