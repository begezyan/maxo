import contextlib
from typing import Any, final

from maxo.routing.ctx import Ctx
from maxo.routing.interfaces.middleware import BaseMiddleware, NextMiddleware
from maxo.routing.signals.update import MaxoUpdate

FACADE_KEY = "facade"


class FacadeMiddleware(BaseMiddleware[MaxoUpdate[Any]]):
    @final
    async def __call__(
        self,
        update: MaxoUpdate[Any],
        ctx: Ctx,
        next: NextMiddleware[MaxoUpdate[Any]],
    ) -> Any:
        with contextlib.suppress(KeyError, AttributeError):
            update.update.bot = update.bot
            ctx[FACADE_KEY] = update.update.facade

        return await next(ctx)
