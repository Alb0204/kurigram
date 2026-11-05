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
from pyrogram import raw, types, utils


class EditMessageWidgetData:
    async def edit_message_widget_data(
        self: pyrogram.Client,
        chat_id: int | str,
        message_id: int,
        public_data: str | None = None,
        chat_data: str | None = None,
    ) -> types.Message:
        """Edit the state of a widget message.

        Clients showing the widget receive the new state without the message being marked as edited.

        .. include:: /_includes/usable-by/bots.rst

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.

            message_id (``int``):
                Identifier of the widget message to edit.

            public_data (``str``, *optional*):
                New state of the widget visible wherever it is shown, including forwards.
                Up to 1024 bytes of text. Pass an empty string to clear it, or leave it out to keep it.

            chat_data (``str``, *optional*):
                New state of the widget visible only in the chat of the message.
                Up to 1024 bytes of text. Pass an empty string to clear it, or leave it out to keep it.

        Returns:
            :obj:`~pyrogram.types.Message`: On success, the edited widget message is returned.

        Example:
            .. code-block:: python

                await app.edit_message_widget_data(chat_id, message_id, chat_data="score=4")
        """
        r = await self.invoke(
            raw.functions.messages.EditMessageWidgetData(
                peer=await self.resolve_peer(chat_id),
                id=message_id,
                public_data=public_data,
                chat_data=chat_data,
            )
        )

        messages = await utils.parse_messages(client=self, messages=r)

        if not messages:
            msg = "The response contains no edited message"
            raise ValueError(msg)

        return messages[0]
