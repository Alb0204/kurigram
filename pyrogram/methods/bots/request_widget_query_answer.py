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
from pyrogram import raw


class RequestWidgetQueryAnswer:
    async def request_widget_query_answer(
        self: pyrogram.Client,
        chat_id: int | str,
        message_id: int,
        data: str | bytes,
        timeout: int = 15,
    ) -> str | None:
        """Send a query to the bot of a widget message, as the widget does when it is tapped.

        This is the equivalent of the widget asking its bot, and only works for a widget whose
        :obj:`~pyrogram.types.Widget` ``can_send_queries`` is True.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.

            message_id (``int``):
                Identifier of the widget message.

            data (``str`` | ``bytes``):
                Data to send to the bot, 1-64 bytes.

            timeout (``int``, *optional*):
                Timeout in seconds. The server waits for the bot for 15 seconds.
                Defaults to 15.

        Returns:
            ``str`` | ``None``: The result the bot answered with, or None if it answered with none.

        Example:
            .. code-block:: python

                result = await app.request_widget_query_answer(chat_id, message_id, "tap")
        """
        r = await self.invoke(
            raw.functions.messages.GetBotWidgetQueryAnswer(
                peer=await self.resolve_peer(chat_id),
                msg_id=message_id,
                query_type=raw.types.WidgetQueryTypeData(),
                # Telegram only wants bytes, but strings are accepted too.
                data=data.encode() if isinstance(data, str) else data,
            ),
            retries=1,
            timeout=timeout,
        )

        return r.result
