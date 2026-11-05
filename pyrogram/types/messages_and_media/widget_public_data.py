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

from pyrogram import raw

from ..object import Object


class WidgetPublicData(Object):
    """The public state of a shared widget, as returned by :meth:`~pyrogram.Client.get_widget_public_data`.

    Parameters:
        period (``int``):
            How often, in seconds, the server recommends polling the state again.

        is_modified (``bool``):
            True, if the state changed from the one the passed hash describes, in which case
            ``data`` and ``hash`` are set.

        data (``str``, *optional*):
            The public state of the widget.

        hash (``int``, *optional*):
            Hash of ``data``, to pass to the next call.
    """

    def __init__(
        self,
        *,
        period: int,
        is_modified: bool,
        data: str | None = None,
        hash: int | None = None,
    ):
        super().__init__()

        self.period = period
        self.is_modified = is_modified
        self.data = data
        self.hash = hash

    @staticmethod
    def _parse(public_data: raw.base.messages.WidgetPublicData) -> WidgetPublicData:
        if isinstance(public_data, raw.types.messages.WidgetPublicData):
            return WidgetPublicData(
                period=public_data.period,
                is_modified=True,
                data=public_data.data,
                hash=public_data.hash,
            )

        return WidgetPublicData(period=public_data.period, is_modified=False)
