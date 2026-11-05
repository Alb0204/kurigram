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
from pyrogram import raw, types


class GetWidgetPublicData:
    async def get_widget_public_data(
        self: pyrogram.Client,
        chat_id: int | str,
        message_id: int,
        hash: int = 0,
    ) -> types.WidgetPublicData:
        """Get the current public state of a shared widget, as clients following it live do.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.

            message_id (``int``):
                Identifier of the widget message.

            hash (``int``, *optional*):
                Hash of the public state already known, from :obj:`~pyrogram.types.Widget`
                ``public_data_hash`` or a previous call. The state is only returned if it changed.
                Defaults to 0, which always returns it.

        Returns:
            :obj:`~pyrogram.types.WidgetPublicData`: The public state, or only the poll period
            if it did not change.

        Example:
            .. code-block:: python

                state = await app.get_widget_public_data(chat_id, message_id)

                state = await app.get_widget_public_data(chat_id, message_id, state.hash)
        """
        r = await self.invoke(
            raw.functions.messages.GetWidgetPublicData(
                peer=await self.resolve_peer(chat_id),
                msg_id=message_id,
                hash=hash,
            )
        )

        return types.WidgetPublicData._parse(r)
