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

import datetime as dt
from io import BytesIO
from typing import Final

import pytest

from pyrogram import raw, types
from pyrogram.methods.messages.get_transcription_languages import GetTranscriptionLanguages
from pyrogram.methods.messages.transcribe_audio_file import TranscribeAudioFile

_UPLOADED: Final[raw.types.InputFile] = raw.types.InputFile(
    id=1, parts=1, name="voice.ogg", md5_checksum=""
)
_PEER: Final[raw.types.InputPeerUser] = raw.types.InputPeerUser(user_id=7, access_hash=0)


class FakeClient(TranscribeAudioFile, GetTranscriptionLanguages):
    """A client that uploads nothing and answers with the response it was built with."""

    def __init__(self, response: object) -> None:
        self.response = response
        self.sent: list[raw.core.TLObject] = []
        self.uploaded: list[object] = []

    async def save_file(self, path: object) -> raw.types.InputFile:
        self.uploaded.append(path)
        return _UPLOADED

    async def resolve_peer(self, peer_id: int | str) -> raw.base.InputPeer:
        return _PEER

    async def invoke(self, query: raw.core.TLObject) -> object:
        self.sent.append(query)
        return self.response


@pytest.mark.asyncio
async def test_an_audio_file_is_uploaded_and_its_transcription_returned() -> None:
    audio = BytesIO(b"OggS")
    client = FakeClient(
        raw.types.messages.TranscribedAudio(
            transcription_id=5,
            text="hel",
            pending=True,
            trial_remains_num=2,
            trial_remains_until_date=1_700_000_000,
        )
    )

    transcribed = await client.transcribe_audio_file(audio)

    assert client.uploaded == [audio]
    assert [query.write() for query in client.sent] == [
        raw.functions.messages.TranscribeAudioFile(file=_UPLOADED).write()
    ]
    assert isinstance(transcribed, types.TranscribedAudio)
    assert (transcribed.id, transcribed.text, transcribed.is_pending) == (5, "hel", True)
    assert transcribed.trial_remains_count == 2
    assert transcribed.trial_remains_until_date == dt.datetime.fromtimestamp(1_700_000_000)


@pytest.mark.asyncio
async def test_a_finished_transcription_is_not_pending() -> None:
    client = FakeClient(raw.types.messages.TranscribedAudio(transcription_id=5, text="hello"))

    transcribed = await client.transcribe_audio_file("voice.ogg")

    assert transcribed.is_pending is False
    assert transcribed.trial_remains_until_date is None


@pytest.mark.parametrize(("chat_id", "peer"), [(None, None), (7, _PEER)])
@pytest.mark.asyncio
async def test_the_languages_are_asked_for_a_chat_only_when_given_one(
    chat_id: int | None, peer: raw.base.InputPeer | None
) -> None:
    client = FakeClient(["en", "it"])

    assert await client.get_transcription_languages(chat_id) == ["en", "it"]

    assert [query.write() for query in client.sent] == [
        raw.functions.messages.GetTranscriptionLangs(peer=peer).write()
    ]
