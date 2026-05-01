"""Тесты MessageManager - закрывают п.1 issue #110 (skip get_message_by_id после edit_message)."""
from unittest.mock import AsyncMock

import pytest

from maxo.dialogs.api.entities import NewMessage, OldMessage, ShowMode
from maxo.dialogs.manager.message_manager import MessageManager
from maxo.enums import ChatType
from maxo.types import InlineKeyboardAttachment, Recipient


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


def _make_old_message_with_kbd(mid: str = "55") -> OldMessage:
    return OldMessage(
        recipient=Recipient(chat_type=ChatType.DIALOG, user_id=1, chat_id=1),
        message_id=mid,
        sequence_id=int(mid),
        text="x",
        attachments=[InlineKeyboardAttachment.factory(buttons=[])],
    )


@pytest.mark.asyncio
async def test_remove_inline_kbd_returns_message_id_str() -> None:
    """remove_inline_kbd теперь возвращает str (message_id), не Message."""
    bot = AsyncMock()
    bot.edit_message = AsyncMock()
    bot.get_message_by_id = AsyncMock()
    mgr = MessageManager(media_id_storage=AsyncMock())

    result = await mgr.remove_inline_kbd(bot, _make_old_message_with_kbd(mid="55"))

    bot.edit_message.assert_awaited_once()
    bot.get_message_by_id.assert_not_called()
    assert result == "55"


@pytest.mark.asyncio
async def test_remove_kbd_no_update_returns_none() -> None:
    """remove_kbd с ShowMode.NO_UPDATE возвращает None."""
    mgr = MessageManager(media_id_storage=AsyncMock())
    result = await mgr.remove_kbd(
        bot=AsyncMock(),
        show_mode=ShowMode.NO_UPDATE,
        old_message=None,
    )
    assert result is None


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
