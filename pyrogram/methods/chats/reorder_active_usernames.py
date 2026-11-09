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

from __future__ import annotations as _annotations

import pyrogram
from pyrogram import raw, utils


class ReorderActiveUsernames:
    async def reorder_active_usernames(
        self: pyrogram.Client, chat_id: int | str, usernames: list[str]
    ) -> bool:
        """Changes order of active usernames of the chat.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                For your personal cloud (Saved Messages) you can simply use "me" or "self".

            usernames (List of ``str``):
                The new order of active usernames.
                All currently active usernames must be specified.

        Returns:
            ``bool``: On success, True is returned.

        Example:
            .. code-block:: python

                # Reorder active usernames of the current user.
                await app.reorder_active_usernames("me", ["kurigram", "kurigrambot"])
        """
        peer = await self.resolve_peer(chat_id)

        if isinstance(peer, raw.types.InputPeerSelf):
            return await self.invoke(raw.functions.account.ReorderUsernames(order=usernames))
        elif isinstance(peer, utils.PEERS_WITH_A_USER_ID):
            return await self.invoke(
                raw.functions.bots.ReorderUsernames(
                    bot=utils.get_input_user_or_channel(peer), order=usernames
                )
            )
        elif isinstance(peer, utils.PEERS_WITH_A_CHANNEL_ID):
            return await self.invoke(
                raw.functions.channels.ReorderUsernames(
                    channel=utils.get_input_user_or_channel(peer), order=usernames
                )
            )
        else:
            raise ValueError("Invalid peer type")
