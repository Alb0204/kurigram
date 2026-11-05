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


class EditSharedWidgetData:
    async def edit_shared_widget_data(
        self: pyrogram.Client,
        widget_id: int,
        public_data: str,
        cache_time: int | None = None,
    ) -> bool:
        """Edit the public state of a shared widget, for every message and forward showing it.

        This works even when every message carrying the widget has been deleted.
        A shared widget can be edited at most once per second.

        .. include:: /_includes/usable-by/bots.rst

        Parameters:
            widget_id (``int``):
                Identifier of the shared widget: :obj:`~pyrogram.types.Widget` ``id`` of a message
                sent with :meth:`~pyrogram.Client.send_widget` and ``is_shared=True``.

            public_data (``str``):
                New public state of the widget, up to 1024 bytes of text.
                Pass an empty string to clear it.

            cache_time (``int``, *optional*):
                How often, in seconds, clients that follow the widget live should poll its public state.
                The server clamps it to 5-3600 seconds; 0 sets it back to the default of 30 seconds.
                Leave it out to keep the current value.

        Returns:
            ``bool``: On success, True is returned.

        Example:
            .. code-block:: python

                await app.edit_shared_widget_data(widget_id, "score=4", cache_time=10)
        """
        return await self.invoke(
            raw.functions.messages.EditWidgetData(
                widget_id=widget_id,
                public_data=public_data,
                cache_time=cache_time,
            )
        )
