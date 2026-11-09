#  Kurigram - Telegram MTProto API Client Library for Python
#
#  Copyright (C) 2017-present Dan <https://github.com/delivrance>
#  Copyright (C) 2024-present KurimuzonAkuma <https://github.com/KurimuzonAkuma>
#
#  This file is part of Kurigram.
#
#  Kurigram is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Kurigram is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with Kurigram. If not, see <https://www.gnu.org/licenses/>.

"""Copying a video keeps its cover and start timestamp, or takes new ones.

https://github.com/kurigram-org/kurigram/issues/563: a copy went out as the bare document, so
both were lost.
"""

from __future__ import annotations as _annotations

from datetime import datetime
from typing import TYPE_CHECKING, Any, Final

import pytest

from pyrogram import Client, enums, raw, types
from pyrogram.file_id import FileId, FileType, ThumbnailSource

if TYPE_CHECKING:
    from pyrogram.raw.core import TLObject

_VIDEO_FILE_ID: Final[str] = FileId(
    file_type=FileType.VIDEO,
    dc_id=2,
    media_id=111,
    access_hash=222,
    file_reference=b"ref",
).encode()

_COVER_ID: Final[int] = 333
_COVER_FILE_ID: Final[str] = FileId(
    file_type=FileType.PHOTO,
    dc_id=2,
    media_id=_COVER_ID,
    access_hash=444,
    file_reference=b"ref",
    thumbnail_source=ThumbnailSource.THUMBNAIL,
    thumbnail_file_type=FileType.PHOTO,
    thumbnail_size="x",
    volume_id=0,
    local_id=0,
).encode()

_START: Final[int] = 7
_TARGET: Final[int] = 42


class _Sent(Exception):
    def __init__(self, query: TLObject) -> None:
        self.query = query


@pytest.fixture
def client() -> Client:
    return Client("copy_video_probe", api_id=1, api_hash="0" * 32, in_memory=True)


def a_video_message(client: Client) -> types.Message:
    return types.Message(
        client=client,
        id=1,
        chat=types.Chat(id=1, type=enums.ChatType.PRIVATE),
        media=enums.MessageMediaType.VIDEO,
        video=types.Video(
            file_id=_VIDEO_FILE_ID,
            file_unique_id="video",
            width=1,
            height=1,
            codec="h264",
            duration=1,
            video_cover=types.Photo(
                file_id=_COVER_FILE_ID,
                file_unique_id="cover",
                width=1,
                height=1,
                file_size=1,
                date=datetime(2026, 1, 1),
            ),
            video_start_timestamp=_START,
        ),
    )


@pytest.fixture
def sent_video(client: Client, monkeypatch: pytest.MonkeyPatch) -> dict[str, Any]:
    """The keyword arguments `send_video` is called with."""
    sent: dict[str, Any] = {}

    async def send_video(**kwargs: Any) -> None:
        sent.update(kwargs)

    monkeypatch.setattr(client, "send_video", send_video)

    return sent


async def test_a_copied_video_keeps_its_cover_and_start(
    client: Client, sent_video: dict[str, Any]
) -> None:
    await a_video_message(client).copy(_TARGET)

    assert sent_video["video"] == _VIDEO_FILE_ID
    assert sent_video["video_cover"] == _COVER_FILE_ID
    assert sent_video["video_start_timestamp"] == _START


async def test_a_copied_video_takes_a_new_cover_and_start(
    client: Client, sent_video: dict[str, Any]
) -> None:
    await a_video_message(client).copy(_TARGET, video_cover="cover.jpg", video_start_timestamp=3)

    assert sent_video["video_cover"] == "cover.jpg"
    assert sent_video["video_start_timestamp"] == 3


async def test_a_copied_video_drops_its_cover_on_false(
    client: Client, sent_video: dict[str, Any]
) -> None:
    await a_video_message(client).copy(_TARGET, video_cover=False)

    assert sent_video["video_cover"] is None


async def test_a_copied_video_reaches_the_wire_with_its_cover_and_start(
    client: Client, monkeypatch: pytest.MonkeyPatch
) -> None:
    async def resolve_peer(peer_id: int) -> raw.base.InputPeer:
        return raw.types.InputPeerUser(user_id=peer_id, access_hash=0)

    async def invoke(query: TLObject, *args: Any, **kwargs: Any) -> None:
        raise _Sent(query)

    monkeypatch.setattr(client, "resolve_peer", resolve_peer)
    monkeypatch.setattr(client, "invoke", invoke)

    with pytest.raises(_Sent) as sent:
        await a_video_message(client).copy(_TARGET)

    query = sent.value.query
    assert isinstance(query, raw.functions.messages.SendMedia)
    assert isinstance(query.media, raw.types.InputMediaDocument)
    assert isinstance(query.media.video_cover, raw.types.InputPhoto)
    assert query.media.video_cover.id == _COVER_ID
    assert query.media.video_timestamp == _START


async def test_a_copied_media_group_keeps_each_videos_cover_and_start(
    client: Client, monkeypatch: pytest.MonkeyPatch
) -> None:
    message = a_video_message(client)

    async def get_media_group(chat_id: int, message_id: int) -> list[types.Message]:
        return [message]

    async def resolve_peer(peer_id: int) -> raw.base.InputPeer:
        return raw.types.InputPeerUser(user_id=peer_id, access_hash=0)

    async def invoke(query: TLObject, *args: Any, **kwargs: Any) -> None:
        raise _Sent(query)

    monkeypatch.setattr(client, "get_media_group", get_media_group)
    monkeypatch.setattr(client, "resolve_peer", resolve_peer)
    monkeypatch.setattr(client, "invoke", invoke)

    with pytest.raises(_Sent) as sent:
        await client.copy_media_group(_TARGET, 1, 1)

    query = sent.value.query
    assert isinstance(query, raw.functions.messages.SendMultiMedia)

    (single,) = query.multi_media
    assert isinstance(single.media, raw.types.InputMediaDocument)
    assert isinstance(single.media.video_cover, raw.types.InputPhoto)
    assert single.media.video_cover.id == _COVER_ID
    assert single.media.video_timestamp == _START
