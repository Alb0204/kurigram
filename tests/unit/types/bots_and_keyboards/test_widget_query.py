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

from typing import Final

import pytest

import pyrogram
from pyrogram import enums, filters, raw, types, utils
from pyrogram.dispatcher import Dispatcher
from pyrogram.handlers import WidgetQueryHandler
from pyrogram.methods.bots.answer_widget_query import AnswerWidgetQuery

_USER: Final[raw.types.User] = raw.types.User(id=11, first_name="Ann")
_BOT_CHAT: Final[raw.types.User] = raw.types.User(id=22, first_name="Bot", bot=True)
_INLINE_MESSAGE_ID: Final[raw.types.InputBotInlineMessageID] = raw.types.InputBotInlineMessageID(
    dc_id=4, id=42, access_hash=7
)


def client() -> pyrogram.Client:
    return pyrogram.Client("test", api_id=1, api_hash="0" * 32, in_memory=True)


@pytest.mark.asyncio
async def test_a_query_from_an_original_names_its_chat_and_message() -> None:
    update = raw.types.UpdateBotWidgetQuery(
        query_id=123,
        query_type=raw.types.WidgetQueryTypeData(),
        user_id=_USER.id,
        peer=raw.types.PeerUser(user_id=_USER.id),
        msg_id=5,
        chat_instance=-9,
        chat_type="private",
        data=b"\x01tap",
        widget_id=77,
    )

    query = await types.WidgetQuery._parse(client(), update, {_USER.id: _USER}, {})

    assert query.id == "123"
    assert query.from_user is not None
    assert query.from_user.id == _USER.id
    assert query.chat is not None
    assert query.chat.id == _USER.id
    assert (query.message_id, query.inline_message_id) == (5, None)
    assert (query.chat_instance, query.chat_type) == ("-9", "private")
    assert (query.data, query.widget_id, query.is_from_copy) == (b"\x01tap", 77, False)
    assert query.raw is update


@pytest.mark.asyncio
async def test_a_query_from_an_inline_message_carries_its_packed_id() -> None:
    update = raw.types.UpdateInlineBotWidgetQuery(
        query_id=1,
        query_type=raw.types.WidgetQueryTypeData(),
        user_id=_USER.id,
        inline_message_id=_INLINE_MESSAGE_ID,
        chat_instance=3,
        chat_type="group",
        data=b"x",
    )

    query = await types.WidgetQuery._parse(client(), update, {_USER.id: _USER}, {})

    assert query.inline_message_id == utils.pack_inline_message_id(_INLINE_MESSAGE_ID)
    assert (query.chat, query.message_id, query.widget_id) == (None, None, None)
    assert query.is_from_copy is False


@pytest.mark.asyncio
async def test_a_query_from_a_copy_reveals_only_the_user_the_data_and_the_widget() -> None:
    update = raw.types.UpdateBotWidgetCopyQuery(
        query_id=2,
        query_type=raw.types.WidgetQueryTypeData(),
        user_id=_USER.id,
        data=b"y",
        widget_id=77,
    )

    query = await types.WidgetQuery._parse(client(), update, {_USER.id: _USER}, {})

    assert query.is_from_copy is True
    assert (query.data, query.widget_id) == (b"y", 77)
    assert (query.chat, query.message_id, query.inline_message_id) == (None, None, None)
    assert (query.chat_instance, query.chat_type) == (None, None)


@pytest.mark.asyncio
async def test_a_query_whose_user_is_missing_parses_without_one() -> None:
    update = raw.types.UpdateBotWidgetQuery(
        query_id=3,
        query_type=raw.types.WidgetQueryTypeData(),
        user_id=_USER.id,
        peer=raw.types.PeerUser(user_id=_BOT_CHAT.id),
        msg_id=1,
        chat_instance=0,
        chat_type="private",
        data=b"z",
    )

    query = await types.WidgetQuery._parse(client(), update, {}, {})

    assert (query.from_user, query.chat) == (None, None)


@pytest.mark.parametrize(
    "update",
    [
        raw.types.UpdateBotWidgetQuery(
            query_id=1,
            query_type=raw.types.WidgetQueryTypeData(),
            user_id=_USER.id,
            peer=raw.types.PeerUser(user_id=_USER.id),
            msg_id=5,
            chat_instance=0,
            chat_type="private",
            data=b"x",
        ),
        raw.types.UpdateInlineBotWidgetQuery(
            query_id=1,
            query_type=raw.types.WidgetQueryTypeData(),
            user_id=_USER.id,
            inline_message_id=_INLINE_MESSAGE_ID,
            chat_instance=0,
            chat_type="group",
            data=b"x",
        ),
        raw.types.UpdateBotWidgetCopyQuery(
            query_id=1,
            query_type=raw.types.WidgetQueryTypeData(),
            user_id=_USER.id,
            data=b"x",
            widget_id=77,
        ),
    ],
    ids=["original", "inline", "copy"],
)
@pytest.mark.asyncio
async def test_the_dispatcher_hands_every_widget_query_to_its_handler(
    update: raw.base.Update,
) -> None:
    # `handler_worker` looks the parser up by `type(update)`, as done here.
    parser = Dispatcher(client()).update_parsers[type(update)]

    parsed, handler_type = await parser(update, {_USER.id: _USER}, {})

    assert isinstance(parsed, types.WidgetQuery)
    assert handler_type is WidgetQueryHandler


class FakeClient(AnswerWidgetQuery):
    """A client that keeps the query it was asked to send."""

    def __init__(self) -> None:
        self.sent: raw.functions.messages.SetBotWidgetQueryAnswer | None = None

    async def invoke(self, query: raw.functions.messages.SetBotWidgetQueryAnswer) -> bool:
        self.sent = query
        return True


@pytest.mark.parametrize("result", ["ok", None])
@pytest.mark.asyncio
async def test_answer_widget_query_sends_the_result_by_the_query_id(result: str | None) -> None:
    fake = FakeClient()

    assert await fake.answer_widget_query("123", result=result) is True

    assert fake.sent is not None
    assert (
        fake.sent.write()
        == raw.functions.messages.SetBotWidgetQueryAnswer(query_id=123, result=result).write()
    )


@pytest.mark.asyncio
async def test_the_sender_and_chat_filters_read_a_widget_query() -> None:
    sender = types.User(id=42, username="someone")
    query = types.WidgetQuery(
        id="1",
        from_user=sender,
        data=b"x",
        is_from_copy=False,
        chat=types.Chat(id=42, type=enums.ChatType.PRIVATE),
    )

    assert await filters.user(42)(None, query)
    assert await filters.private(None, query)
