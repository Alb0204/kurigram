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
from pyrogram.methods.chats.toggle_forum_topics import ToggleForumTopics


class FakeClient(ToggleForumTopics):
    """A client that keeps the raw `channels.toggleForum` it was asked to send."""

    def __init__(self) -> None:
        self.sent: raw.functions.channels.ToggleForum | None = None

    async def resolve_peer(self, chat_id):
        return raw.types.InputChannel(channel_id=1, access_hash=0)

    async def invoke(self, query: raw.functions.channels.ToggleForum) -> raw.types.Updates:
        self.sent = query
        return raw.types.Updates(updates=[], users=[], chats=[], date=0, seq=0)


@pytest.mark.asyncio
async def test_the_layer_233_sidebar_field_is_sent_off_by_default() -> None:
    # Layer 233 made `sidebar:Bool` a required field of `channels.toggleForum`.
    client = FakeClient()

    assert await client.toggle_forum_topics(1, is_forum=True) is True

    assert client.sent is not None
    assert client.sent.sidebar is False
    assert client.sent.tabs is False


@pytest.mark.asyncio
async def test_has_forum_sidebar_is_forwarded() -> None:
    client = FakeClient()

    await client.toggle_forum_topics(1, is_forum=True, has_forum_sidebar=True)

    assert client.sent is not None
    assert client.sent.sidebar is True
