from enum import Enum


class Sentinels(Enum):
    UNHANDLED = "<unhandled>"
    REJECTED = "<rejected>"


UNHANDLED = Sentinels.UNHANDLED
REJECTED = Sentinels.REJECTED


class SkipHandler(Exception):
    pass


class CancelHandler(Exception):
    pass
