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

import zlib
from typing import TYPE_CHECKING, Final

from pyrogram import raw

from ..object import Object

if TYPE_CHECKING:
    import pyrogram

# The server refuses widget HTML over 32 KB, so a payload it produced never inflates past this.
#  Capping the output keeps a forged or corrupt payload from inflating without bound.
MAX_WIDGET_HTML_SIZE: Final[int] = 32 * 1024


def inflate_widget_payload(payload: bytes) -> str | None:
    """Return the HTML a widget `payload` carries, or `None` if it is not a valid one.

    The payload is a zlib stream (RFC 1950), not gzip and not raw deflate, holding at most
    32 KB of UTF-8 text.
    """
    inflater = zlib.decompressobj()

    try:
        html = inflater.decompress(payload, MAX_WIDGET_HTML_SIZE + 1)
    except zlib.error:
        return None

    # `eof` is only set once the Adler-32 trailer has been read and checked.
    if len(html) > MAX_WIDGET_HTML_SIZE or not inflater.eof:
        return None

    try:
        return html.decode("utf-8")
    except UnicodeDecodeError:
        return None


class Widget(Object):
    """A widget: a small self-contained HTML document sent by a bot and run by the client.

    Parameters:
        width (``int``):
            Width of the widget in CSS pixels, 0 if it sizes itself.

        height (``int``):
            Height of the widget in CSS pixels, 0 if it sizes itself.

        html (``str``, *optional*):
            HTML source of the widget.
            None if the payload received from the server could not be decompressed, in which
            case the widget should be treated as unsupported media.

        id (``int``, *optional*):
            Identifier of the shared widget, if the widget was sent as a shared one.
            Its public data can be changed with :meth:`~pyrogram.Client.edit_shared_widget_data`.

        public_data (``str``, *optional*):
            State of the widget visible wherever it is shown, including forwards. Up to 1024 bytes.

        public_data_hash (``int``, *optional*):
            Hash of the public data, to pass to :meth:`~pyrogram.Client.get_widget_public_data`.

        chat_data (``str``, *optional*):
            State of the widget visible only in the chat of the original message. Up to 1024 bytes.

        is_copy (``bool``, *optional*):
            True, if the widget is a forwarded copy, which has no chat data.

        can_send_queries (``bool``, *optional*):
            True, if the widget can send queries to the bot when the user taps it.

        can_send_background_queries (``bool``, *optional*):
            True, if the widget can also send queries to the bot while it is visible,
            without a tap.
    """

    def __init__(
        self,
        *,
        client: pyrogram.Client | None = None,
        width: int,
        height: int,
        html: str | None = None,
        id: int | None = None,
        public_data: str | None = None,
        public_data_hash: int | None = None,
        chat_data: str | None = None,
        is_copy: bool | None = None,
        can_send_queries: bool | None = None,
        can_send_background_queries: bool | None = None,
    ):
        super().__init__(client)

        self.width = width
        self.height = height
        self.html = html
        self.id = id
        self.public_data = public_data
        self.public_data_hash = public_data_hash
        self.chat_data = chat_data
        self.is_copy = is_copy
        self.can_send_queries = can_send_queries
        self.can_send_background_queries = can_send_background_queries

    @staticmethod
    def _parse(
        client: pyrogram.Client | None,
        widget: raw.types.MessageMediaWidget | raw.types.BotInlineMessageWidget,
    ) -> Widget:
        is_media = isinstance(widget, raw.types.MessageMediaWidget)

        return Widget(
            width=widget.width,
            height=widget.height,
            html=inflate_widget_payload(widget.payload),
            id=widget.widget_id,
            public_data=widget.public_data,
            public_data_hash=widget.public_data_hash,
            chat_data=widget.chat_data,
            is_copy=bool(widget.is_copy) if is_media else None,
            can_send_queries=bool(widget.can_query) if is_media else None,
            can_send_background_queries=bool(widget.background_query) if is_media else None,
            client=client,
        )
