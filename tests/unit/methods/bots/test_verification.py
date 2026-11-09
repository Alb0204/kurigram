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

"""`verify_user()`, `verify_chat()` and their removals: Bot API 10.4's verification methods.

https://core.telegram.org/bots/api#verifyuser. All four map to `bots.setCustomVerification`.
"""

from __future__ import annotations as _annotations

from typing import TYPE_CHECKING, Any, Final

import pytest

from pyrogram import Client, enums, raw, types

if TYPE_CHECKING:
    from pyrogram.raw.core import TLObject

_PEER: Final = raw.types.InputPeerUser(user_id=42, access_hash=7)


@pytest.fixture
def sent(monkeypatch: pytest.MonkeyPatch) -> tuple[Client, list[TLObject]]:
    client = Client("verification_probe", api_id=1, api_hash="0" * 32, in_memory=True)
    queries: list[TLObject] = []

    async def resolve_peer(peer_id: int | str) -> raw.base.InputPeer:
        return _PEER

    async def invoke(query: TLObject, *args: Any, **kwargs: Any) -> bool:
        queries.append(query)
        return True

    monkeypatch.setattr(client, "resolve_peer", resolve_peer)
    monkeypatch.setattr(client, "invoke", invoke)

    return client, queries


@pytest.mark.parametrize("method", ["verify_user", "verify_chat"])
async def test_verify_sends_no_description_by_default(
    sent: tuple[Client, list[TLObject]], method: str
) -> None:
    client, queries = sent

    assert await getattr(client, method)(42) is True

    (query,) = queries
    assert query.write() == (
        raw.functions.bots.SetCustomVerification(peer=_PEER, enabled=True).write()
    )


async def test_verify_sends_the_description_with_its_text_links(
    sent: tuple[Client, list[TLObject]],
) -> None:
    client, queries = sent

    await client.verify_user(
        42,
        custom_description="Official site",
        custom_description_entities=[
            types.MessageEntity(
                type=enums.MessageEntityType.TEXT_LINK, offset=9, length=4, url="https://a.b"
            )
        ],
    )

    (query,) = queries
    assert query.write() == (
        raw.functions.bots.SetCustomVerification(
            peer=_PEER,
            enabled=True,
            custom_description=raw.types.TextWithEntities(
                text="Official site",
                entities=[raw.types.MessageEntityTextUrl(offset=9, length=4, url="https://a.b")],
            ),
        ).write()
    )


@pytest.mark.parametrize("method", ["remove_user_verification", "remove_chat_verification"])
async def test_remove_verification_disables_it(
    sent: tuple[Client, list[TLObject]], method: str
) -> None:
    client, queries = sent

    assert await getattr(client, method)(42) is True

    (query,) = queries
    assert query.write() == (
        raw.functions.bots.SetCustomVerification(peer=_PEER, enabled=False).write()
    )
