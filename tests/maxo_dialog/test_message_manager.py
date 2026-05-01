"""Тесты MessageManager - закрывают п.1 issue #110 (skip get_message_by_id после edit_message)."""
from unittest.mock import AsyncMock

import pytest

from maxo.dialogs.api.entities import NewMessage, OldMessage
from maxo.dialogs.manager.message_manager import MessageManager
from maxo.enums import ChatType
from maxo.types import Recipient


def _make_old_message(mid: str = "100", text: str = "old text") -> OldMessage:
    return OldMessage(
        recipient=Recipient(chat_type=ChatType.DIALOG, user_id=1, chat_id=1),
        message_id=mid,
        sequence_id=int(mid),
        text=text,
        attachments=[],
    )


def _make_new_message(text: str = "new text") -> NewMessage:
    return NewMessage(
        recipient=Recipient(chat_type=ChatType.DIALOG, user_id=1, chat_id=1),
        text=text,
    )


@pytest.mark.asyncio
async def test_edit_message_does_not_call_get_message_by_id() -> None:
    """edit_message больше не делает рефетч после PUT - синтезирует Message локально."""
    bot = AsyncMock()
    bot.edit_message = AsyncMock()
    bot.get_message_by_id = AsyncMock()
    mgr = MessageManager(media_id_storage=AsyncMock())

    result = await mgr.edit_message(
        bot,
        _make_new_message("new text"),
        _make_old_message(mid="42"),
    )

    bot.edit_message.assert_awaited_once()
    bot.get_message_by_id.assert_not_called()
    assert result.body.mid == "42"
    assert result.body.text == "new text"
