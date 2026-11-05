#  Pyrogram - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-present Dan <https://github.com/delivrance>
#
#  This file is part of Pyrogram.
#
#  Pyrogram is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Pyrogram is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with Pyrogram.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import annotations as _annotations

import base64
import struct
from typing import Final

import pytest

from pyrogram import raw
from pyrogram.methods.messages.edit_inline_widget_data import EditInlineWidgetData
from pyrogram.methods.messages.edit_message_widget_data import EditMessageWidgetData
from pyrogram.methods.messages.edit_shared_widget_data import EditSharedWidgetData

_DC_ID: Final[int] = 4
# The Bot API layout of `inline_message_id`: unpadded url-safe base64 of `<iqq`.
_INLINE_MESSAGE_ID: Final[str] = (
    base64.urlsafe_b64encode(struct.pack("<iqq", _DC_ID, 42, 7)).decode().rstrip("=")
)
_SLEEP_THRESHOLD: Final[float] = 42


class FakeClient(EditMessageWidgetData, EditInlineWidgetData, EditSharedWidgetData):
    """A client that keeps every query it sends and the sessions it asks for."""

    sleep_threshold: float = _SLEEP_THRESHOLD

    def __init__(self) -> None:
        self.sent: list[raw.core.TLObject] = []
        self.sessions: list[tuple[int, bool]] = []

    async def resolve_peer(self, peer_id: int | str) -> raw.base.InputPeer:
        return raw.types.InputPeerUser(user_id=int(peer_id), access_hash=0)

    async def get_session(self, dc_id: int, *, is_media: bool) -> FakeClient:
        self.sessions.append((dc_id, is_media))
        return self

    async def invoke(
        self, query: raw.core.TLObject, sleep_threshold: float | None = None
    ) -> raw.core.TLObject | bool:
        self.sent.append(query)

        if isinstance(query, raw.functions.messages.EditMessageWidgetData):
            return raw.types.Updates(updates=[], users=[], chats=[], date=0, seq=0)

        return True


@pytest.mark.asyncio
async def test_an_edit_leaves_out_the_fields_it_was_not_given() -> None:
    client = FakeClient()

    # The response carries no message, which is the one case the method refuses.
    with pytest.raises(ValueError, match="no edited message"):
        await client.edit_message_widget_data(7, 5, chat_data="")

    # Wire bytes, because `TLObject.__eq__` never compares the type. An empty `chat_data`
    #  clears it and has to be sent; the absent `public_data` keeps its flag unset.
    assert [query.write() for query in client.sent] == [
        raw.functions.messages.EditMessageWidgetData(
            peer=raw.types.InputPeerUser(user_id=7, access_hash=0), id=5, chat_data=""
        ).write()
    ]


@pytest.mark.asyncio
async def test_an_inline_edit_goes_to_the_dc_of_the_inline_message() -> None:
    client = FakeClient()

    assert await client.edit_inline_widget_data(_INLINE_MESSAGE_ID, public_data="p") is True

    assert client.sessions == [(_DC_ID, True)]
    assert [query.write() for query in client.sent] == [
        raw.functions.messages.EditInlineBotMessageWidgetData(
            id=raw.types.InputBotInlineMessageID(dc_id=_DC_ID, id=42, access_hash=7),
            public_data="p",
        ).write()
    ]


@pytest.mark.parametrize("cache_time", [None, 0, 10])
@pytest.mark.asyncio
async def test_a_shared_widget_edit_sends_its_cache_time_only_when_given(
    cache_time: int | None,
) -> None:
    client = FakeClient()

    assert await client.edit_shared_widget_data(99, "score=4", cache_time=cache_time) is True

    assert [query.write() for query in client.sent] == [
        raw.functions.messages.EditWidgetData(
            widget_id=99, public_data="score=4", cache_time=cache_time
        ).write()
    ]


def test_a_cache_time_of_0_and_an_empty_data_are_sent_rather_than_dropped() -> None:
    # 0 sets the period back to 30 s and `""` clears the data, so neither may write the
    #  same bytes as leaving the field out.
    def edit(**kwargs: int) -> bytes:
        return raw.functions.messages.EditWidgetData(widget_id=1, public_data="x", **kwargs).write()

    def chat_edit(**kwargs: str) -> bytes:
        return raw.functions.messages.EditMessageWidgetData(
            peer=raw.types.InputPeerSelf(), id=1, **kwargs
        ).write()

    assert edit(cache_time=0) != edit()
    assert chat_edit(chat_data="") != chat_edit()
