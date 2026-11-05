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

from pyrogram import raw, types, utils

from ..object import Object
from ..update import Update

if TYPE_CHECKING:
    import pyrogram


class WidgetQuery(Object, Update):
    """A query sent to the bot by a widget.

    It comes from an original widget message, from a widget message sent via the bot in inline
    mode, or from a forwarded copy of a shared widget. A copy reveals only the user, the data and
    the widget identifier.

    Parameters:
        id (``str``):
            Unique identifier for this query, to pass to :meth:`~pyrogram.Client.answer_widget_query`
            within 15 seconds.

        from_user (:obj:`~pyrogram.types.User`):
            User who sent the query.

        data (``bytes``):
            Data sent by the widget, 1-64 bytes.

        is_from_copy (``bool``):
            True, if the query comes from a forwarded copy of a shared widget, in which case
            only ``widget_id`` tells which widget sent it.

        chat (:obj:`~pyrogram.types.Chat`, *optional*):
            Chat of the widget message, if it was not sent via the bot in inline mode and the
            query does not come from a copy.

        message_id (``int``, *optional*):
            Identifier of the widget message in ``chat``.

        inline_message_id (``str``, *optional*):
            Identifier of the widget message sent via the bot in inline mode.

        chat_instance (``str``, *optional*):
            Global identifier, uniquely corresponding to the chat the widget message is in.

        chat_type (``str``, *optional*):
            Type of the chat the widget message is in, as Telegram names it (``"private"``,
            ``"group"``, ...), kept as a string because it can name types no enum lists yet.

        widget_id (``int``, *optional*):
            Identifier of the shared widget, if the widget is a shared one.

        raw (:obj:`~pyrogram.raw.base.Update`, *optional*):
            The raw update, which also carries the query type and wallet details layer 233
            defines for TON wallet requests.
    """

    def __init__(
        self,
        *,
        client: pyrogram.Client | None = None,
        id: str,
        from_user: types.User | None,
        data: bytes,
        is_from_copy: bool,
        chat: types.Chat | None = None,
        message_id: int | None = None,
        inline_message_id: str | None = None,
        chat_instance: str | None = None,
        chat_type: str | None = None,
        widget_id: int | None = None,
        raw: (
            raw.types.UpdateBotWidgetQuery
            | raw.types.UpdateInlineBotWidgetQuery
            | raw.types.UpdateBotWidgetCopyQuery
            | None
        ) = None,
    ):
        super().__init__(client)

        self.id = id
        self.from_user = from_user
        self.data = data
        self.is_from_copy = is_from_copy
        self.chat = chat
        self.message_id = message_id
        self.inline_message_id = inline_message_id
        self.chat_instance = chat_instance
        self.chat_type = chat_type
        self.widget_id = widget_id
        self.raw = raw

    @staticmethod
    async def _parse(
        client: pyrogram.Client,
        update: raw.types.UpdateBotWidgetQuery
        | raw.types.UpdateInlineBotWidgetQuery
        | raw.types.UpdateBotWidgetCopyQuery,
        users: dict[int, raw.base.User],
        chats: dict[int, raw.base.Chat],
    ) -> WidgetQuery:
        chat = None
        message_id = None
        inline_message_id = None
        chat_instance = None
        chat_type = None

        if isinstance(update, raw.types.UpdateBotWidgetQuery):
            raw_peer_id = utils.get_raw_peer_id(update.peer)
            peer = (
                users.get(raw_peer_id)
                if isinstance(update.peer, raw.types.PeerUser)
                else chats.get(raw_peer_id)
            )
            chat = await types.Chat._parse_chat(client, peer) if peer is not None else None
            message_id = update.msg_id
            chat_instance = str(update.chat_instance)
            chat_type = update.chat_type
        elif isinstance(update, raw.types.UpdateInlineBotWidgetQuery):
            inline_message_id = utils.pack_inline_message_id(update.inline_message_id)
            chat_instance = str(update.chat_instance)
            chat_type = update.chat_type

        user = users.get(update.user_id)

        return WidgetQuery(
            id=str(update.query_id),
            from_user=await types.User._parse(client, user) if user is not None else None,
            data=update.data,
            is_from_copy=isinstance(update, raw.types.UpdateBotWidgetCopyQuery),
            chat=chat,
            message_id=message_id,
            inline_message_id=inline_message_id,
            chat_instance=chat_instance,
            chat_type=chat_type,
            widget_id=update.widget_id,
            raw=update,
            client=client,
        )

    async def answer(self, result: str | None = None) -> bool:
        """Bound method *answer* of :obj:`~pyrogram.types.WidgetQuery`.

        Use this method as a shortcut for:

        .. code-block:: python

            await client.answer_widget_query(widget_query.id, result="ok")

        Example:
            .. code-block:: python

                await widget_query.answer("ok")

        Parameters:
            result (``str``, *optional*):
                Text handed back to the widget that sent the query, up to 1024 bytes.
                Omit it to answer with no result.

        Returns:
            ``bool``: True, on success.
        """
        return await self._client.answer_widget_query(widget_query_id=self.id, result=result)
