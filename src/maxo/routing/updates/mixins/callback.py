from abc import abstractmethod

from maxo.omit import Omittable, Omitted
from maxo.routing.updates.mixins.subscription import SubscriptionMethodsFacade
from maxo.types.callback import Callback
from maxo.types.new_message_body import NewMessageBody
from maxo.types.simple_query_result import SimpleQueryResult


class CallbackMethodsFacade(SubscriptionMethodsFacade):
    __slots__ = ()

    @property
    @abstractmethod
    def callback(self) -> Callback:
        raise NotImplementedError

    async def callback_answer(
        self,
        notification: Omittable[str | None] = Omitted(),
        message: NewMessageBody | None = None,
    ) -> SimpleQueryResult:
        return await self.bot.answer_on_callback(
            callback_id=self.callback.callback_id,
            notification=notification,
            message=message,
        )
