from logging import getLogger

from maxo.dialogs import ChatEvent
from maxo.dialogs.api.entities import Context, Stack
from maxo.dialogs.api.protocols import StackAccessValidator
from maxo.enums import ChatType
from maxo.routing.ctx import Ctx
from maxo.routing.middlewares.update_context import EVENT_CHAT_KEY, EVENT_FROM_USER_KEY

logger = getLogger(__name__)


class DefaultAccessValidator(StackAccessValidator):
    async def is_allowed(
        self,
        stack: Stack,
        context: Context | None,
        event: ChatEvent,
        ctx: Ctx,
    ) -> bool:
        access_settings = context.access_settings if context else stack.access_settings

        if not access_settings:
            return True
        chat = ctx.get(EVENT_CHAT_KEY)
        # У maxo нет ChatType.PRIVATE, аналог - ChatType.DIALOG
        if chat is not None and chat.type is ChatType.DIALOG:
            return True
        if access_settings.user_ids:
            user = ctx.get(EVENT_FROM_USER_KEY)
            # Пост в канале без user - не пройдёт user_ids, но не AttributeError
            if user is None or user.id not in access_settings.user_ids:
                return False
        return True
