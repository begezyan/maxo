"""Тесты параллельной обработки callback в Dialog._callback_handler - закрывает п.2 issue #110."""
import asyncio
import uuid
from datetime import UTC, datetime
from unittest.mock import AsyncMock, MagicMock

import pytest

from maxo.dialogs.dialog import Dialog
from maxo.dialogs.utils import CB_SEP
from maxo.routing.updates import MessageCallback
from maxo.types import Callback, User


def _make_user() -> User:
    return User(
        first_name="Test",
        is_bot=False,
        last_activity_time=datetime.now(UTC),
        user_id=1,
    )


def _make_callback(payload: str) -> MessageCallback:
    return MessageCallback(
        timestamp=datetime.now(UTC),
        callback=Callback(
            timestamp=datetime.now(UTC),
            callback_id=str(uuid.uuid4()),
            payload=payload,
            user=_make_user(),
        ),
        message=MagicMock(),
        user_locale="ru",
    )


def _make_dialog_manager(*, show_coro=None, answer_coro=None) -> MagicMock:
    dialog_manager = MagicMock()
    dialog_manager.show = show_coro if show_coro else AsyncMock()
    dialog_manager.answer_callback = answer_coro if answer_coro else AsyncMock()
    dialog_manager.current_context = MagicMock(return_value=MagicMock())
    dialog_manager.middleware_data = {}
    return dialog_manager


def _make_dialog(*, need_refresh: bool = True) -> MagicMock:
    window = AsyncMock()
    window.process_callback = AsyncMock(return_value=True)
    dialog = MagicMock(spec=Dialog)
    dialog._current_window = AsyncMock(return_value=window)
    dialog._need_refresh = MagicMock(return_value=need_refresh)
    return dialog


@pytest.mark.asyncio
async def test_callback_calls_show_and_answer_when_refresh_needed() -> None:
    """Sanity: при _need_refresh=True вызываются и show, и answer_callback."""
    dialog_manager = _make_dialog_manager()
    dialog = _make_dialog(need_refresh=True)
    callback = _make_callback(f"intentid{CB_SEP}payload")

    await Dialog._callback_handler(dialog, callback, ctx={}, dialog_manager=dialog_manager)

    dialog_manager.show.assert_awaited_once()
    dialog_manager.answer_callback.assert_awaited_once()


@pytest.mark.asyncio
async def test_callback_only_answer_when_no_refresh() -> None:
    """Если _need_refresh=False - вызывается только answer_callback."""
    dialog_manager = _make_dialog_manager()
    dialog = _make_dialog(need_refresh=False)
    callback = _make_callback(f"intentid{CB_SEP}payload")

    await Dialog._callback_handler(dialog, callback, ctx={}, dialog_manager=dialog_manager)

    dialog_manager.show.assert_not_called()
    dialog_manager.answer_callback.assert_awaited_once()


@pytest.mark.asyncio
async def test_callback_show_and_answer_run_in_parallel() -> None:
    """show и answer_callback должны выполняться параллельно (gather), не последовательно."""

    async def slow_show() -> None:
        await asyncio.sleep(0.1)

    async def slow_answer() -> None:
        await asyncio.sleep(0.1)

    dialog_manager = _make_dialog_manager(show_coro=slow_show, answer_coro=slow_answer)
    dialog = _make_dialog(need_refresh=True)
    callback = _make_callback(f"intentid{CB_SEP}payload")

    start = asyncio.get_event_loop().time()
    await Dialog._callback_handler(dialog, callback, ctx={}, dialog_manager=dialog_manager)
    elapsed = asyncio.get_event_loop().time() - start

    # Sequential = ~0.2s, parallel = ~0.1s. Порог 0.15s.
    assert elapsed < 0.15, f"expected parallel (~0.1s), got {elapsed:.3f}s"
