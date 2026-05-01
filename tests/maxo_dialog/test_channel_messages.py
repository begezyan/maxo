"""Тесты обработки сообщений из каналов (без sender.user) - закрывает issue #111."""
from typing import Any

import pytest

from maxo.dialogs.api.entities import EventContext
from maxo.dialogs.api.entities.events import EVENT_CONTEXT_KEY
from maxo.dialogs.test_tools import BotClient, MockMessageManager
from maxo.enums import ChatType
from maxo import Dispatcher, Router


@pytest.fixture
def captured_ctx() -> dict[str, Any]:
    return {}


@pytest.fixture
def message_manager() -> MockMessageManager:
    return MockMessageManager()


@pytest.fixture
def dp(message_manager: MockMessageManager, captured_ctx: dict[str, Any]) -> Dispatcher:
    from maxo.dialogs import setup_dialogs

    router = Router()

    @router.message_created()
    async def handler(event, ctx):
        captured_ctx["event_context"] = ctx[EVENT_CONTEXT_KEY]

    dp = Dispatcher()
    dp.include_router(router)
    setup_dialogs(dp, message_manager=message_manager)
    return dp


@pytest.fixture
def channel_client(dp: Dispatcher) -> BotClient:
    return BotClient(dp, user_id=1, chat_id=-100, chat_type=ChatType.CHANNEL)


@pytest.mark.asyncio
async def test_storage_proxy_channel_message_created(
    channel_client: BotClient,
    captured_ctx: dict[str, Any],
) -> None:
    """MessageCreated без sender.user не должен падать в storage_proxy."""
    await channel_client.send_channel_post("Привет канал")

    ev_ctx: EventContext = captured_ctx["event_context"]
    assert ev_ctx.user is None
    assert ev_ctx.user_id is None
    assert ev_ctx.chat_id == -100
    assert ev_ctx.chat_type == ChatType.CHANNEL
