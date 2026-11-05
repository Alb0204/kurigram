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

from pyrogram import raw, types
from pyrogram.methods.bots.request_widget_query_answer import RequestWidgetQueryAnswer
from pyrogram.methods.messages.get_widget_public_data import GetWidgetPublicData

_PEER = raw.types.InputPeerUser(user_id=7, access_hash=0)


class FakeClient(RequestWidgetQueryAnswer, GetWidgetPublicData):
    """A client that answers each query with the response it was built with."""

    def __init__(self, response: raw.core.TLObject) -> None:
        self.response = response
        self.sent: list[tuple[raw.core.TLObject, dict]] = []

    async def resolve_peer(self, peer_id: int | str) -> raw.base.InputPeer:
        return _PEER

    async def invoke(self, query: raw.core.TLObject, **kwargs) -> raw.core.TLObject:
        self.sent.append((query, kwargs))
        return self.response


@pytest.mark.parametrize("data", ["tap", b"tap"])
@pytest.mark.asyncio
async def test_a_widget_query_sends_its_data_as_bytes_and_returns_the_result(
    data: str | bytes,
) -> None:
    client = FakeClient(raw.types.messages.BotWidgetQueryAnswer(result="ok"))

    assert await client.request_widget_query_answer(7, 5, data) == "ok"

    (query, kwargs), *rest = client.sent
    assert rest == []
    assert (
        query.write()
        == raw.functions.messages.GetBotWidgetQueryAnswer(
            peer=_PEER, msg_id=5, query_type=raw.types.WidgetQueryTypeData(), data=b"tap"
        ).write()
    )
    assert kwargs == {"retries": 1, "timeout": 15}


@pytest.mark.asyncio
async def test_an_answer_without_a_result_is_none() -> None:
    client = FakeClient(raw.types.messages.BotWidgetQueryAnswer())

    assert await client.request_widget_query_answer(7, 5, b"x") is None


@pytest.mark.asyncio
async def test_changed_public_data_comes_back_with_its_hash() -> None:
    client = FakeClient(raw.types.messages.WidgetPublicData(hash=9, data="score=4", period=30))

    state = await client.get_widget_public_data(7, 5)

    assert isinstance(state, types.WidgetPublicData)
    assert (state.is_modified, state.data, state.hash, state.period) == (True, "score=4", 9, 30)
    (query, _), *_ = client.sent
    assert (
        query.write()
        == raw.functions.messages.GetWidgetPublicData(peer=_PEER, msg_id=5, hash=0).write()
    )


@pytest.mark.asyncio
async def test_unchanged_public_data_comes_back_with_only_the_period() -> None:
    client = FakeClient(raw.types.messages.WidgetPublicDataNotModified(period=60))

    state = await client.get_widget_public_data(7, 5, hash=9)

    assert (state.is_modified, state.data, state.hash, state.period) == (False, None, None, 60)
