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


class SendSharedWidget:
    async def send_shared_widget(
        self: pyrogram.Client,
        chat_id: int | str,
        widget_id: int,
        chat_data: str | None = None,
        caption: str = "",
        parse_mode: enums.ParseMode | None = None,
        caption_entities: list[types.MessageEntity] | None = None,
        disable_notification: bool | None = None,
        message_thread_id: int | None = None,
        reply_parameters: types.ReplyParameters | None = None,
        protect_content: bool | None = None,
        allow_paid_broadcast: bool | None = None,
        business_connection_id: str | None = None,
        reply_markup: (
            types.InlineKeyboardMarkup
            | types.ReplyKeyboardMarkup
            | types.ReplyKeyboardRemove
            | types.ForceReply
            | None
        ) = None,
    ) -> types.Message | None:
        """Send a shared widget again, by its identifier.

        The new message shows the same widget, and the same public state, as every other
        message carrying it.

        .. include:: /_includes/usable-by/bots.rst

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.

            widget_id (``int``):
                Identifier of the shared widget: :obj:`~pyrogram.types.Widget` ``id`` of a message
                sent with :meth:`~pyrogram.Client.send_widget` and ``is_shared=True``.

            chat_data (``str``, *optional*):
                State of the widget visible only in this chat. Up to 1024 bytes of text.

            caption (``str``, *optional*):
                Text shown by clients that cannot display widgets.

            parse_mode (:obj:`~pyrogram.enums.ParseMode`, *optional*):
                By default, texts are parsed using both Markdown and HTML styles.
                You can combine both syntaxes together.

            caption_entities (List of :obj:`~pyrogram.types.MessageEntity`, *optional*):
                List of special entities that appear in the caption, which can be specified instead of *parse_mode*.

            disable_notification (``bool``, *optional*):
                Sends the message silently.
                Users will receive a notification with no sound.

            message_thread_id (``int``, *optional*):
                Unique identifier for the target message thread (topic) of the forum.
                For supergroups only.

            reply_parameters (:obj:`~pyrogram.types.ReplyParameters`, *optional*):
                Describes reply parameters for the message that is being sent.

            protect_content (``bool``, *optional*):
                Protects the contents of the sent message from forwarding and saving.

            allow_paid_broadcast (``bool``, *optional*):
                If True, you will be allowed to send up to 1000 messages per second.
                Ignoring broadcasting limits for a fee of 0.1 Telegram Stars per message.
                The relevant Stars will be withdrawn from the bot's balance.

            business_connection_id (``str``, *optional*):
                Unique identifier of the business connection on behalf of which the message will be sent.

            reply_markup (:obj:`~pyrogram.types.InlineKeyboardMarkup` | :obj:`~pyrogram.types.ReplyKeyboardMarkup` | :obj:`~pyrogram.types.ReplyKeyboardRemove` | :obj:`~pyrogram.types.ForceReply`, *optional*):
                Additional interface options. An object for an inline keyboard, custom reply keyboard,
                instructions to remove reply keyboard or to force a reply from the user.

        Returns:
            :obj:`~pyrogram.types.Message` | ``None``: On success, the sent widget message is returned, otherwise,
            in case the server answered with no message, None is returned.

        Example:
            .. code-block:: python

                sent = await app.send_widget(chat_id, html, is_shared=True)

                await app.send_shared_widget(other_chat_id, sent.widget.id)
        """
        r = await self.invoke(
            raw.functions.messages.SendMedia(
                peer=await self.resolve_peer(chat_id),
                media=raw.types.InputMediaWidgetId(widget_id=widget_id, chat_data=chat_data),
                silent=disable_notification,
                reply_to=await utils.get_reply_to(self, reply_parameters, message_thread_id),
                random_id=self.rnd_id(),
                noforwards=protect_content,
                allow_paid_floodskip=allow_paid_broadcast,
                reply_markup=await reply_markup.write(self) if reply_markup else None,
                **await utils.parse_text_entities(self, caption, parse_mode, caption_entities),
            ),
            business_connection_id=business_connection_id,
        )

        messages = await utils.parse_messages(client=self, messages=r)

        return messages[0] if messages else None
