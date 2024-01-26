from __future__ import annotations

from contextlib import contextmanager
from math import ceil
from typing import Iterator, Generator

from unicodedata import category, east_asian_width

from ..geometry import Coordinate
from ..input import parse_escape_code, read_characters
from ..text import Characters, AnsiEscapeSequence, AnsiEscapeSequences, Text
from ..utilities import terminal_inputs, WorkerProcess, SupportsString


class Cursor:
    position: Coordinate = Coordinate(0, 0)

    @classmethod
    def get_live_position(cls, *rival_workers: WorkerProcess) -> Coordinate:
        with terminal_inputs():
            for worker in rival_workers:
                worker.pause()
            AnsiEscapeSequences.REQUEST_LIVE_CURSOR_POSITION.value.execute()
            read_characters(2)  # TODO: Deal with mouse movement case
            raw_position = parse_escape_code(lambda c: c == "R")[:-1]
            for worker in rival_workers:
                worker.resume()
            return Coordinate(*map(int, reversed(raw_position.split(";")))) - (1, 1)

    @classmethod
    def up(cls, n: int = 1) -> type[Cursor]:
        if not isinstance(n, int):
            raise NotImplementedError from None
        AnsiEscapeSequences.CURSOR_UP.value(n=n).execute()
        cls.position -= (0, n)
        return cls

    @classmethod
    def down(cls, n: int = 1) -> type[Cursor]:
        if not isinstance(n, int):
            raise NotImplementedError from None
        AnsiEscapeSequences.CURSOR_DOWN.value(n=n).execute()
        cls.position += (0, n)
        return cls

    @classmethod
    def left(cls, n: int = 1) -> type[Cursor]:
        if not isinstance(n, int):
            raise NotImplementedError from None
        AnsiEscapeSequences.CURSOR_LEFT.value(n=n).execute()
        cls.position -= (n, 0)
        return cls

    @classmethod
    def right(cls, n: int = 1) -> type[Cursor]:
        if not isinstance(n, int):
            raise NotImplementedError from None
        AnsiEscapeSequences.CURSOR_RIGHT.value(n=n).execute()
        cls.position += (n, 0)
        return cls

    @classmethod
    def retreat(cls) -> type[Cursor]:
        return cls.go_to(Coordinate(0, cls.position.y))

    @classmethod
    def go_to(cls, coordinate: Coordinate | tuple[int, int]) -> type[Cursor]:
        if not isinstance(coordinate, (Coordinate, tuple)):
            raise NotImplementedError from None
        elif isinstance(coordinate, tuple) and tuple(map(type, coordinate)) != (int, int):
            raise NotImplementedError from None
        coordinate = coordinate if isinstance(coordinate, Coordinate) else Coordinate(*coordinate)
        AnsiEscapeSequences.CURSOR_GO_TO.value(coordinate).execute()
        cls.position = coordinate
        return cls

    @classmethod
    def sync_position(cls) -> None:
        cls.position = cls.get_live_position()

    @classmethod
    def show(cls) -> type[Cursor]:
        AnsiEscapeSequences.CURSOR_VISIBILITY.value(on=True).execute()
        return cls

    @classmethod
    def hide(cls) -> type[Cursor]:
        AnsiEscapeSequences.CURSOR_VISIBILITY.value(on=False).execute()
        return cls

    @classmethod
    def clear_line(cls, *, before_cursor: bool = True, after_cursor: bool = True) -> type[Cursor]:
        if before_cursor and after_cursor:
            AnsiEscapeSequences.CLEAR_LINE.value.execute()
        elif before_cursor:
            AnsiEscapeSequences.CLEAR_LINE_LEFT.value.execute()
        elif after_cursor:
            AnsiEscapeSequences.CLEAR_LINE_RIGHT.value.execute()
        return cls

    @classmethod
    @contextmanager
    def in_position(cls, position: Coordinate) -> Iterator[type[Cursor]]:
        old_position = cls.position
        cls.go_to(position)
        try:
            yield cls
        finally:
            cls.position = old_position

    @classmethod
    def get_print_displacement(cls, object_: SupportsString) -> Generator[tuple[str, Coordinate], None, Coordinate]:
        text = Text.as_text(object_)
        largest_width = 0
        width = 0
        height = 0
        east_asian_width_lookup = {
            'N': 1,
            'Na': 1,
            'H': 1,
            'A': 1,
            'F': 2,
            'W': 2,
        }
        for character in text:
            match character:
                case _ if isinstance(character, AnsiEscapeSequence):
                    width += character.cursor_print_displacement.x
                    height += character.cursor_print_displacement.y
                case Characters.NEWLINE:
                    if width > largest_width:
                        largest_width = width
                    width = 0
                    height += 1
                case Characters.TAB:
                    cursor_x = Cursor.position.x + width
                    width += int(ceil(cursor_x / 4)) * 4 - cursor_x
                case Characters.BACKSPACE:
                    width -= 1
                case Characters.CARRIAGE_RETURN:
                    width = 0
                case _ if category(character)[0] in "MC":
                    pass
                case _:
                    width += east_asian_width_lookup[east_asian_width(character)]
            yield str(character), Coordinate(width, height)
        largest_width = width
        return Coordinate(max(width, largest_width), height)


Cursor.position = Cursor.get_live_position()
