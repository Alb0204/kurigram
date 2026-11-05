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


class AnswerWidgetQuery:
    async def answer_widget_query(
        self: pyrogram.Client,
        widget_query_id: str,
        result: str | None = None,
    ) -> bool:
        """Answer a query sent to the bot by a widget.

        The answer goes only to the client that sent the query, and must be sent within
        15 seconds of it.

        .. include:: /_includes/usable-by/bots.rst

        Parameters:
            widget_query_id (``str``):
                Unique identifier of the query to be answered.

            result (``str``, *optional*):
                Text handed back to the widget, up to 1024 bytes.
                Omit it to answer with no result.

        Returns:
            ``bool``: True, on success.

        Example:
            .. code-block:: python

                @app.on_widget_query()
                async def on_widget_query(client, widget_query):
                    await client.answer_widget_query(widget_query.id, result="ok")
        """
        return await self.invoke(
            raw.functions.messages.SetBotWidgetQueryAnswer(
                query_id=int(widget_query_id), result=result
            )
        )
