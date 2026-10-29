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

import sqlite3
from pathlib import Path
from typing import Any

import pytest

from pyrogram.storage import sqlite_storage
from pyrogram.storage.sqlite_storage import SQLiteStorage


@pytest.mark.asyncio
async def test_conn_property_round_trips_the_connection() -> None:
    # self.conn moved from a plain attribute (declared non-Optional via a
    #  `# type:` comment but assigned None in __init__) to a property backed by
    #  self._conn, so open()/close() and every query still have to see the same
    #  connection object through the ordinary self.conn read/write syntax.
    storage = SQLiteStorage("test", Path(), in_memory=True)

    await storage.open()
    assert await storage.is_bot() is None

    await storage.date(0)
    assert await storage.date() == 0

    await storage.close()


def test_conn_raises_before_open() -> None:
    storage = SQLiteStorage("test", Path(), in_memory=True)

    with pytest.raises(RuntimeError):
        _ = storage.conn


@pytest.mark.asyncio
@pytest.mark.parametrize(("do_vacuum", "vacuumed"), [(True, True), (False, False)])
async def test_open_vacuums_a_session_file_only_when_asked_to(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    *,
    do_vacuum: bool,
    vacuumed: bool,
) -> None:
    statements: list[str] = []
    connect = sqlite3.connect

    # The connection is made inside `open()`, so the trace goes on it as it is made.
    def traced_connect(*args: Any, **kwargs: Any) -> sqlite3.Connection:
        connection = connect(*args, **kwargs)
        connection.set_trace_callback(statements.append)
        return connection

    monkeypatch.setattr(sqlite_storage.sqlite3, "connect", traced_connect)

    storage = SQLiteStorage("test", tmp_path, do_vacuum=do_vacuum)

    await storage.open()
    await storage.close()

    assert ("VACUUM" in statements) is vacuumed
