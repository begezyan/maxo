from typing import Any

from maxo.routing.ctx import Ctx
from maxo.routing.interfaces.middleware import BaseMiddleware, NextMiddleware
from maxo.routing.signals.update import Update
from maxo.routing.updates.base import BaseUpdate
from maxo.routing.updates.bot_started import BotStarted
from maxo.routing.updates.message_callback import MessageCallback
from maxo.routing.updates.message_created import MessageCreated
from maxo.types import User

# TODO: Объединить с UpdateContextMiddleware

EVENT_FROM_USER_KEY = "event_from_user"


class EventContextMiddleware(BaseMiddleware[Update[Any]]):
    async def __call__(
        self,
        update: Update[Any],
        ctx: Ctx,
        next: NextMiddleware[Update[Any]],
    ) -> Any:
        user = self._resolve_event_context(update.update)
        if user is not None:
            ctx[EVENT_FROM_USER_KEY] = user
        return await next(ctx)

    def _resolve_event_context(
        self,
        update: BaseUpdate,
    ) -> User | None:
        if isinstance(update, MessageCreated):
            return update.message.sender
        if isinstance(update, MessageCallback):
            return update.callback.user
        if isinstance(update, BotStarted):
            return update.user
        # TODO: Остальные ивенты
        return None
