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
async def test_remove_inline_kbd_skips_refetch() -> None:
    """remove_inline_kbd не делает get_message_by_id после edit."""
    bot = AsyncMock()
    bot.edit_message = AsyncMock()
    bot.get_message_by_id = AsyncMock()
    mgr = MessageManager(media_id_storage=AsyncMock())

    result = await mgr.remove_inline_kbd(bot, _make_old_message_with_kbd(mid="55"))

    bot.edit_message.assert_awaited_once()
    bot.get_message_by_id.assert_not_called()
    assert result is None


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
    """edit_message больше не делает рефетч и не возвращает Message."""
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
    assert result is None


@pytest.mark.asyncio
async def test_edit_message_safe_returns_old_message_without_refetch() -> None:
    """edit_message_safe строит OldMessage напрямую из new + старого id, без рефетча."""
    bot = AsyncMock()
    bot.edit_message = AsyncMock()
    bot.get_message_by_id = AsyncMock()
    mgr = MessageManager(media_id_storage=AsyncMock())

    result = await mgr.edit_message_safe(
        bot,
        _make_new_message("new text"),
        _make_old_message(mid="42"),
    )

    bot.edit_message.assert_awaited_once()
    bot.get_message_by_id.assert_not_called()
    assert isinstance(result, OldMessage)
    assert result.message_id == "42"
    assert result.text == "new text"
