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

import pytest

from pyrogram import raw
from pyrogram.methods.messages.send_shared_widget import SendSharedWidget
from pyrogram.methods.messages.send_widget import SendWidget
from pyrogram.parser import Parser


class FakeClient(SendWidget, SendSharedWidget):
    """A client that keeps the `messages.SendMedia` it was asked to send."""

    def __init__(self) -> None:
        self.parser = Parser(None)
        self.sent: raw.functions.messages.SendMedia | None = None

    def rnd_id(self) -> int:
        return 1

    async def resolve_peer(self, peer_id: int | str) -> raw.base.InputPeer:
        return raw.types.InputPeerUser(user_id=int(peer_id), access_hash=0)

    async def invoke(
        self,
        query: raw.functions.messages.SendMedia,
        business_connection_id: str | None = None,
    ) -> raw.base.messages.Messages:
        self.sent = query

        return raw.types.messages.Messages(messages=[], chats=[], users=[], topics=[])


@pytest.mark.asyncio
async def test_send_widget_sends_the_html_as_text_with_its_options() -> None:
    client = FakeClient()

    await client.send_widget(
        7,
        "<p>hi</p>",
        width=320,
        height=0,
        allow_queries=True,
        is_shared=True,
        public_data="score=0",
        chat_data="room=1",
        caption="Update your app to see this widget.",
    )

    assert client.sent is not None
    # Bots never send compressed bytes: the server compresses the HTML itself.
    assert client.sent.media == raw.types.InputMediaWidget(
        width=320,
        height=0,
        html="<p>hi</p>",
        allow_queries=True,
        shared_widget=True,
        public_data="score=0",
        chat_data="room=1",
    )
    assert client.sent.message == "Update your app to see this widget."


@pytest.mark.asyncio
async def test_send_widget_leaves_every_option_unset_by_default() -> None:
    client = FakeClient()

    await client.send_widget(7, "<p>hi</p>")

    assert client.sent is not None
    assert client.sent.media == raw.types.InputMediaWidget(width=0, height=0, html="<p>hi</p>")
    assert client.sent.message == ""


@pytest.mark.asyncio
async def test_send_shared_widget_refers_to_the_widget_by_its_id() -> None:
    client = FakeClient()

    await client.send_shared_widget(7, 99, chat_data="room=2")

    assert client.sent is not None
    assert client.sent.media == raw.types.InputMediaWidgetId(widget_id=99, chat_data="room=2")
