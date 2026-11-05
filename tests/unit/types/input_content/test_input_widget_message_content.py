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

from pyrogram import Client, enums, raw, types


def client() -> Client:
    return Client(name="widget_content", in_memory=True)


@pytest.mark.asyncio
async def test_a_widget_result_writes_the_html_its_options_and_its_caption() -> None:
    content = types.InputWidgetMessageContent(
        "<p>hi</p>",
        width=320,
        allow_queries=True,
        is_shared=True,
        public_data="p",
        chat_data="c",
        caption="**Update** your app",
        parse_mode=enums.ParseMode.MARKDOWN,
        show_caption_above_media=True,
    )

    written = await content.write(client(), None)

    assert isinstance(written, raw.types.InputBotInlineMessageWidget)
    assert (
        written.write()
        == raw.types.InputBotInlineMessageWidget(
            width=320,
            height=0,
            html="<p>hi</p>",
            allow_queries=True,
            shared_widget=True,
            invert_media=True,
            public_data="p",
            chat_data="c",
            message="Update your app",
            entities=[raw.types.MessageEntityBold(offset=0, length=6)],
        ).write()
    )


@pytest.mark.asyncio
async def test_a_shared_widget_result_refers_to_the_widget_by_its_id() -> None:
    markup = types.InlineKeyboardMarkup([[types.InlineKeyboardButton("Open", callback_data="o")]])
    content = types.InputSharedWidgetMessageContent(99, chat_data="c")

    written = await content.write(client(), markup)

    assert isinstance(written, raw.types.InputBotInlineMessageWidgetId)
    assert (
        written.write()
        == raw.types.InputBotInlineMessageWidgetId(
            widget_id=99,
            chat_data="c",
            reply_markup=await markup.write(client()),
            message="",
            entities=None,
        ).write()
    )
