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

import pyrogram
from pyrogram import raw, utils


class EditInlineWidgetData:
    async def edit_inline_widget_data(
        self: pyrogram.Client,
        inline_message_id: str,
        public_data: str | None = None,
        chat_data: str | None = None,
    ) -> bool:
        """Edit the state of a widget message sent via the bot in inline mode.

        .. include:: /_includes/usable-by/bots.rst

        Parameters:
            inline_message_id (``str``):
                Identifier of the inline message.

            public_data (``str``, *optional*):
                New state of the widget visible wherever it is shown, including forwards.
                Up to 1024 bytes of text. Pass an empty string to clear it, or leave it out to keep it.

            chat_data (``str``, *optional*):
                New state of the widget visible only in the chat of the message.
                Up to 1024 bytes of text. Pass an empty string to clear it, or leave it out to keep it.

        Returns:
            ``bool``: On success, True is returned.

        Example:
            .. code-block:: python

                await app.edit_inline_widget_data(inline_message_id, public_data="score=4")
        """
        unpacked = utils.unpack_inline_message_id(inline_message_id)

        session = await self.get_session(unpacked.dc_id, is_media=True)

        return await session.invoke(
            raw.functions.messages.EditInlineBotMessageWidgetData(
                id=unpacked,
                public_data=public_data,
                chat_data=chat_data,
            ),
            sleep_threshold=self.sleep_threshold,
        )
