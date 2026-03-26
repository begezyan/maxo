from collections.abc import Callable
from datetime import UTC, datetime
from typing import Any

import pytest

from maxo.enums import ChatType
from maxo.routing.ctx import Ctx
from maxo.routing.dispatcher import Dispatcher
from maxo.routing.filters import BaseFilter
from maxo.routing.interfaces import NextMiddleware
from maxo.routing.routers.simple import Router
from maxo.routing.sentinels import UNHANDLED
from maxo.routing.signals import BeforeStartup
from maxo.routing.updates.message_created import MessageCreated
from maxo.types import Message, MessageBody, Recipient, User


@pytest.fixture
def update() -> MessageCreated:
    return MessageCreated(
        message=Message(
            body=MessageBody(mid="test", seq=1),
            recipient=Recipient(chat_type=ChatType.DIALOG, chat_id=1),
            timestamp=datetime.now(UTC),
            sender=User(
                user_id=1,
                first_name="Test",
                is_bot=False,
                last_activity_time=datetime.now(UTC),
            ),
        ),
        timestamp=datetime.now(UTC),
    )


def middleware_factory(name: str) -> Callable[..., Any]:
    async def middleware(
        update: MessageCreated,
        ctx: Ctx,
        next: NextMiddleware[MessageCreated],
    ) -> Any:
        ctx["execution_order"].append(name)
        return await next(ctx)

    return middleware


@pytest.mark.asyncio
async def test_router_filter_false_skips_router_inner_middleware(ctx: Ctx) -> None:
    dp = Dispatcher()
    router = Router("child")
    dp.include(router)

    class RouterFilter(BaseFilter[MessageCreated]):
        async def __call__(self, update: MessageCreated, ctx: Ctx) -> bool:
            ctx["execution_order"].append("filter")
            return False

    async def handler(_: Any, ctx: Ctx) -> str:
        ctx["execution_order"].append("handler")
        return "OK"

    router.message_created.filter(RouterFilter())
    router.message_created.middleware.inner.add(middleware_factory("inner"))
    router.message_created.handler(handler)

    await dp.feed_signal(BeforeStartup())
    ctx["execution_order"] = []
    result = await dp.trigger(ctx)

    assert result is UNHANDLED
    assert ctx["execution_order"] == ["filter"]


@pytest.mark.asyncio
async def test_first_router_inner_middleware_skipped_second_router_handles(
    ctx: Ctx,
) -> None:
    dp = Dispatcher()
    first_router = Router("first")
    second_router = Router("second")
    dp.include(first_router, second_router)

    class FirstRouterFilter(BaseFilter[MessageCreated]):
        async def __call__(self, update: MessageCreated, ctx: Ctx) -> bool:
            ctx["execution_order"].append("first_filter")
            return False

    class SecondRouterFilter(BaseFilter[MessageCreated]):
        async def __call__(self, update: MessageCreated, ctx: Ctx) -> bool:
            ctx["execution_order"].append("second_filter")
            return True

    async def second_handler(_: Any, ctx: Ctx) -> str:
        ctx["execution_order"].append("second_handler")
        return "OK"

    first_router.message_created.filter(FirstRouterFilter())
    first_router.message_created.middleware.inner.add(middleware_factory("first_inner"))
    second_router.message_created.filter(SecondRouterFilter())
    second_router.message_created.handler(second_handler)

    await dp.feed_signal(BeforeStartup())
    ctx["execution_order"] = []
    result = await dp.trigger(ctx)

    assert result == "OK"
    assert ctx["execution_order"] == [
        "first_filter",
        "second_filter",
        "second_handler",
    ]
