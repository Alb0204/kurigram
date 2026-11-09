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

"""`resolve_peer()` falling back to a message a `min` peer was seen in.

https://core.telegram.org/api/min. The server accepts such a peer only while it still knows the
message, so of several sightings the most recent one is the one to send.
"""

from __future__ import annotations as _annotations

from types import SimpleNamespace
from typing import Final

from pyrogram import Client, enums, raw, utils

_USER: Final[int] = 777001
_OLD_GROUP: Final[int] = 1111111
_NEW_GROUP: Final[int] = 2222222


def a_message_from_the_user_in(group: int, message_id: int) -> SimpleNamespace:
    """The parts of a parsed `Message` the fallback reads."""
    return SimpleNamespace(
        chat=SimpleNamespace(
            type=enums.ChatType.SUPERGROUP,
            raw=SimpleNamespace(access_hash=group * 10),
        ),
        raw=raw.types.Message(
            id=message_id,
            peer_id=raw.types.PeerChannel(channel_id=group),
            from_id=raw.types.PeerUser(user_id=_USER),
            date=0,
            message="",
        ),
        from_user=SimpleNamespace(id=_USER, username=None, usernames=None, phone_number=None),
        sender_chat=None,
    )


async def test_the_most_recent_sighting_is_used() -> None:
    client = Client("min_peer_probe", api_id=1, api_hash="0" * 32, in_memory=True)

    await client.message_cache.set(
        (utils.get_channel_id(_OLD_GROUP), 5), a_message_from_the_user_in(_OLD_GROUP, 5)
    )
    await client.message_cache.set(
        (utils.get_channel_id(_NEW_GROUP), 9), a_message_from_the_user_in(_NEW_GROUP, 9)
    )

    peer = await client._resolve_peer_from_message_cache(_USER)

    assert peer == raw.types.InputPeerUserFromMessage(
        peer=raw.types.InputPeerChannel(channel_id=_NEW_GROUP, access_hash=_NEW_GROUP * 10),
        msg_id=9,
        user_id=_USER,
    )
