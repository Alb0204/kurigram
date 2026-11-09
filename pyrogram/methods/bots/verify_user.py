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
from pyrogram import enums, raw, types, utils


class VerifyUser:
    async def verify_user(
        self: pyrogram.Client,
        user_id: int | str,
        custom_description: str | None = None,
        custom_description_parse_mode: enums.ParseMode | None = None,
        custom_description_entities: list[types.MessageEntity] | None = None,
    ) -> bool:
        """Verify a user on behalf of the organization the bot represents.

        .. include:: /_includes/usable-by/bots.rst

        Parameters:
            user_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target user.

            custom_description (``str``, *optional*):
                Custom description for the verification, 0-70 characters.
                Must be empty if the organization isn't allowed to provide a custom verification
                description.

            custom_description_parse_mode (:obj:`~pyrogram.enums.ParseMode`, *optional*):
                By default, texts are parsed using both Markdown and HTML styles.
                You can combine both syntaxes together.
                Only text links are supported.

            custom_description_entities (List of :obj:`~pyrogram.types.MessageEntity`, *optional*):
                List of special entities that appear in the custom description, which can be
                specified instead of *custom_description_parse_mode*.
                Only text links are supported.

        Returns:
            ``bool``: On success, True is returned.

        Example:
            .. code-block:: python

                await app.verify_user(123456789)

                await app.verify_user(123456789, custom_description="Official account")
        """
        text, entities = (
            await utils.parse_text_entities(
                self,
                custom_description or "",
                custom_description_parse_mode,
                custom_description_entities,
            )
        ).values()

        return await self.invoke(
            raw.functions.bots.SetCustomVerification(
                peer=await self.resolve_peer(user_id),
                enabled=True,
                custom_description=raw.types.TextWithEntities(text=text, entities=entities or [])
                if text
                else None,
            )
        )
