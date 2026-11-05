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

import gzip
import zlib
from typing import Final

import pytest

import pyrogram
from pyrogram import enums, raw, types
from pyrogram.types.messages_and_media.widget import (
    MAX_WIDGET_HTML_SIZE,
    inflate_widget_payload,
)

_HTML: Final[str] = "<!doctype html><p>Café ☕</p>"
_PAYLOAD: Final[bytes] = zlib.compress(_HTML.encode(), 9)
_CHANNEL_ID: Final[int] = 1000000000


def raw_deflate(data: bytes) -> bytes:
    compressor = zlib.compressobj(9, zlib.DEFLATED, -zlib.MAX_WBITS)
    return compressor.compress(data) + compressor.flush()


def test_a_zlib_payload_inflates_to_its_html() -> None:
    assert inflate_widget_payload(_PAYLOAD) == _HTML


@pytest.mark.parametrize(
    "payload",
    [
        # The doc names both as the formats a client must not accept in place of RFC 1950.
        pytest.param(gzip.compress(_HTML.encode()), id="gzip"),
        pytest.param(raw_deflate(_HTML.encode()), id="raw-deflate"),
        pytest.param(_PAYLOAD[:-4], id="missing-adler32"),
        pytest.param(_PAYLOAD[:-1] + bytes([_PAYLOAD[-1] ^ 1]), id="wrong-adler32"),
        pytest.param(zlib.compress(b"\xff\xfe<p>"), id="not-utf-8"),
        pytest.param(b"", id="empty"),
    ],
)
def test_a_payload_that_is_not_a_valid_widget_inflates_to_none(payload: bytes) -> None:
    assert inflate_widget_payload(payload) is None


def test_a_payload_inflating_past_32_kb_is_refused() -> None:
    at_limit = zlib.compress(b"a" * MAX_WIDGET_HTML_SIZE)
    over_limit = zlib.compress(b"a" * (MAX_WIDGET_HTML_SIZE + 1))

    assert inflate_widget_payload(at_limit) == "a" * MAX_WIDGET_HTML_SIZE
    assert inflate_widget_payload(over_limit) is None


@pytest.mark.asyncio
async def test_a_widget_message_parses_into_message_widget() -> None:
    media = raw.types.MessageMediaWidget(
        width=320,
        height=0,
        payload=_PAYLOAD,
        can_query=True,
        public_data="score=3",
        public_data_hash=42,
        chat_data="room=1",
        widget_id=7,
    )
    message = raw.types.Message(
        id=1,
        peer_id=raw.types.PeerChannel(channel_id=_CHANNEL_ID),
        date=0,
        message="",
        media=media,
        entities=[],
        restriction_reason=[],
    )
    client = pyrogram.Client("test", api_id=1, api_hash="0" * 32, in_memory=True)

    parsed = await types.Message._parse(client, message, users={}, chats={})

    assert parsed.media == enums.MessageMediaType.WIDGET
    widget = parsed.widget
    assert widget is not None
    assert (widget.width, widget.height, widget.html) == (320, 0, _HTML)
    assert (widget.id, widget.public_data, widget.public_data_hash) == (7, "score=3", 42)
    assert widget.chat_data == "room=1"
    assert widget.can_send_queries is True
    assert widget.can_send_background_queries is False
    assert widget.is_copy is False
