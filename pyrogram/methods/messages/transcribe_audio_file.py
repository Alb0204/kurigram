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

from typing import TYPE_CHECKING, BinaryIO

import pyrogram
from pyrogram import raw, types

if TYPE_CHECKING:
    from pyrogram._typing import PathType


class TranscribeAudioFile:
    async def transcribe_audio_file(
        self: pyrogram.Client,
        audio: PathType | BinaryIO,
    ) -> types.TranscribedAudio:
        """Recognize the speech in an audio file, without sending it to any chat.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            audio (``str`` | :obj:`os.PathLike` | ``BinaryIO``):
                Audio file to upload and transcribe, as a path on the local file system or a
                file-like object opened in binary mode.

        Returns:
            :obj:`~pyrogram.types.TranscribedAudio`: The transcription. If it is still pending,
            the final text arrives later as a raw update.

        Example:
            .. code-block:: python

                transcribed = await app.transcribe_audio_file("voice.ogg")
                print(transcribed.text)
        """
        r = await self.invoke(
            raw.functions.messages.TranscribeAudioFile(file=await self.save_file(audio))
        )

        return types.TranscribedAudio._parse(r)
