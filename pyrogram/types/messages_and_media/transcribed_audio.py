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

from pyrogram import utils

from ..object import Object

if TYPE_CHECKING:
    import datetime as dt

    from pyrogram import raw


class TranscribedAudio(Object):
    """The speech recognition result of an audio file.

    Parameters:
        id (``int``):
            Identifier of the transcription.

        text (``str``):
            The recognized text, so far if the transcription is still pending.

        is_pending (``bool``):
            True, if the transcription is not finished yet. The final text arrives later as a
            raw ``UpdateTranscribedAudioFile`` update carrying the same ``id``, which
            :meth:`~pyrogram.Client.on_raw_update` receives.

        trial_remains_count (``int``, *optional*):
            Number of free transcriptions left, for users without Telegram Premium.

        trial_remains_until_date (:py:obj:`~datetime.datetime`, *optional*):
            Date when the free transcriptions are refilled.
    """

    def __init__(
        self,
        *,
        id: int,
        text: str,
        is_pending: bool,
        trial_remains_count: int | None = None,
        trial_remains_until_date: dt.datetime | None = None,
    ):
        super().__init__()

        self.id = id
        self.text = text
        self.is_pending = is_pending
        self.trial_remains_count = trial_remains_count
        self.trial_remains_until_date = trial_remains_until_date

    @staticmethod
    def _parse(transcribed: raw.types.messages.TranscribedAudio) -> TranscribedAudio:
        return TranscribedAudio(
            id=transcribed.transcription_id,
            text=transcribed.text,
            is_pending=bool(transcribed.pending),
            trial_remains_count=transcribed.trial_remains_num,
            trial_remains_until_date=utils.timestamp_to_datetime(
                transcribed.trial_remains_until_date
            ),
        )
