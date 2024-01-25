from __future__ import annotations

from sys import stdout, stdin
from contextlib import contextmanager
from typing import Iterator

from ..geometry import Coordinate
from ..input import parse_escape_code, read_characters, InputLock
from ..utilities import console_inputs


class Cursor:
    position: Coordinate = Coordinate(0, 0)
    visible: bool = True

    @classmethod
    def get_live_position(cls) -> Coordinate:
        with console_inputs():
            with InputLock.acquire(2):
                stdout.write("\033[6n")
                stdout.flush()
                stdin.flush()
                read_characters(2, lock_priority=None)
                raw_position = parse_escape_code(lambda c: c == "R", lock_priority=None)[:-1]
        return Coordinate(*map(int, reversed(raw_position.split(";")))) - (1, 1)

    @classmethod
    def up(cls, n: int = 1) -> type[Cursor]:
        if not isinstance(n, int):
            raise NotImplementedError from None
        stdout.write(f"\033[{n}A")
        stdout.flush()
        cls.position -= (0, n)
        return cls

    @classmethod
    def down(cls, n: int = 1) -> type[Cursor]:
        if not isinstance(n, int):
            raise NotImplementedError from None
        stdout.write(f"\033[{n}B")
        stdout.flush()
        cls.position += (0, n)
        return cls

    @classmethod
    def left(cls, n: int = 1) -> type[Cursor]:
        if not isinstance(n, int):
            raise NotImplementedError from None
        stdout.write(f"\033[{n}D")
        stdout.flush()
        cls.position -= (n, 0)
        return cls

    @classmethod
    def retreat(cls) -> type[Cursor]:
        return cls.go_to(Coordinate(0, cls.position.y))

    @classmethod
    def right(cls, n: int = 1) -> type[Cursor]:
        if not isinstance(n, int):
            raise NotImplementedError from None
        stdout.write(f"\033[{n}C")
        stdout.flush()
        cls.position += (n, 0)
        return cls

    @classmethod
    def go_to(cls, coordinate: Coordinate | tuple[int, int]) -> type[Cursor]:
        if not isinstance(coordinate, (Coordinate, tuple)):
            raise NotImplementedError from None
        elif isinstance(coordinate, tuple) and tuple(map(type, coordinate)) != (int, int):
            raise NotImplementedError from None
        coordinate = coordinate if isinstance(coordinate, Coordinate) else Coordinate(*coordinate)
        stdout.write(f"\033[{coordinate.y + 1};{coordinate.x + 1}H")
        stdout.flush()
        cls.position = coordinate
        return cls

    @classmethod
    def sync_position(cls) -> None:
        cls.position = cls.get_live_position()

    @classmethod
    def show(cls) -> type[Cursor]:
        stdout.write("\033[?25h")
        stdout.flush()
        cls.visible = True
        return cls

    @classmethod
    def hide(cls) -> type[Cursor]:
        stdout.write("\033[?25l")
        stdout.flush()
        cls.visible = False
        return cls

    @staticmethod
    def clear_line(before_cursor: bool = True, after_cursor: bool = True) -> None:
        if not (before_cursor or after_cursor):
            return
        elif not before_cursor:
            stdout.write("\033[K")
        elif not after_cursor:
            stdout.write("\033[1K")
        else:
            stdout.write("\033[2K")
        stdout.flush()

    @classmethod
    @contextmanager
    def in_position(cls, position: Coordinate) -> Iterator[type[Cursor]]:
        old_position = cls.position
        cls.go_to(position)
        try:
            yield cls
        finally:
            cls.position = old_position


Cursor.position = Cursor.get_live_position()
