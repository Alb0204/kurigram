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

from typing import TYPE_CHECKING

from pyrogram import raw, utils

from .input_message_content import InputMessageContent

if TYPE_CHECKING:
    import pyrogram
    from pyrogram import enums, types


class InputWidgetMessageContent(InputMessageContent):
    """Content of a widget message to be sent as the result of an inline query.

    Parameters:
        html (``str``):
            Source of the widget: one HTML document with inline CSS and JavaScript, and
            ``data:`` images only. At most 32 KB, and at most 4 KB once the server has
            compressed it.

        width (``int``, *optional*):
            Width of the widget in CSS pixels. 0 lets the widget size itself.
            Defaults to 0.

        height (``int``, *optional*):
            Height of the widget in CSS pixels. 0 lets the widget size itself.
            Defaults to 0.

        allow_queries (``bool``, *optional*):
            Pass True to let the widget send queries to the bot.

        is_shared (``bool``, *optional*):
            Pass True to make the widget a shared one.

        public_data (``str``, *optional*):
            State of the widget visible wherever it is shown, including forwards.
            Up to 1024 bytes of text.

        chat_data (``str``, *optional*):
            State of the widget visible only in the chat the message is sent to.
            Up to 1024 bytes of text.

        caption (``str``, *optional*):
            Text shown by clients that cannot display widgets.

        parse_mode (:obj:`~pyrogram.enums.ParseMode`, *optional*):
            By default, texts are parsed using both Markdown and HTML styles.
            You can combine both syntaxes together.

        caption_entities (List of :obj:`~pyrogram.types.MessageEntity`, *optional*):
            List of special entities that appear in the caption, which can be specified instead of *parse_mode*.

        show_caption_above_media (``bool``, *optional*):
            Pass True to show the caption above the widget.
    """

    def __init__(
        self,
        html: str,
        width: int = 0,
        height: int = 0,
        allow_queries: bool | None = None,
        is_shared: bool | None = None,
        public_data: str | None = None,
        chat_data: str | None = None,
        caption: str = "",
        parse_mode: enums.ParseMode | None = None,
        caption_entities: list[types.MessageEntity] | None = None,
        show_caption_above_media: bool | None = None,
    ):
        super().__init__()

        self.html = html
        self.width = width
        self.height = height
        self.allow_queries = allow_queries
        self.is_shared = is_shared
        self.public_data = public_data
        self.chat_data = chat_data
        self.caption = caption
        self.parse_mode = parse_mode
        self.caption_entities = caption_entities
        self.show_caption_above_media = show_caption_above_media

    async def write(self, client: pyrogram.Client, reply_markup):
        return raw.types.InputBotInlineMessageWidget(
            width=self.width,
            height=self.height,
            html=self.html,
            allow_queries=self.allow_queries,
            shared_widget=self.is_shared,
            invert_media=self.show_caption_above_media,
            public_data=self.public_data,
            chat_data=self.chat_data,
            reply_markup=await reply_markup.write(client) if reply_markup else None,
            **await utils.parse_text_entities(
                client, self.caption, self.parse_mode, self.caption_entities
            ),
        )
