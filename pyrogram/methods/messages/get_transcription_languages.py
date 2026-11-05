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


class GetTranscriptionLanguages:
    async def get_transcription_languages(
        self: pyrogram.Client,
        chat_id: int | str | None = None,
    ) -> list[str]:
        """Get the languages speech can be transcribed from.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            chat_id (``int`` | ``str``, *optional*):
                Unique identifier (int) or username (str) of a chat, to get the languages
                available in it.

        Returns:
            List of ``str``: The language codes.

        Example:
            .. code-block:: python

                languages = await app.get_transcription_languages()
        """
        return await self.invoke(
            raw.functions.messages.GetTranscriptionLangs(
                peer=await self.resolve_peer(chat_id) if chat_id is not None else None
            )
        )
