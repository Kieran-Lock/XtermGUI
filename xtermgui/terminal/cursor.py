from __future__ import annotations

from contextlib import contextmanager
from dataclasses import dataclass, field
from math import ceil
from typing import Iterator, Generator, TYPE_CHECKING

from unicodedata import category, east_asian_width

from ..geometry import Coordinate
from ..input import parse_escape_code, read_characters
from ..text import Characters, AnsiEscapeSequence, AnsiEscapeSequences, Text, CharacterInfo
from ..utilities import WorkerProcess, SupportsString, Singleton

if TYPE_CHECKING:
    from .terminal import Terminal


@dataclass(slots=True)
class Cursor(metaclass=Singleton):
    terminal: Terminal = field(repr=False)
    position: Coordinate = field(init=False, default=Coordinate(0, 0))

    def get_live_position(self, *rival_workers: WorkerProcess) -> Coordinate:
        with self.terminal.setup_inputs():
            for worker in rival_workers:
                worker.pause()
            AnsiEscapeSequences.REQUEST_LIVE_CURSOR_POSITION.execute()
            read_characters(2)
            raw_position = parse_escape_code(lambda c: c == "R")[:-1]
            for worker in rival_workers:
                worker.resume()
            return Coordinate(*map(int, reversed(raw_position.split(";")))) - (1, 1)

    def up(self, n: int = 1) -> type[Cursor]:
        if not isinstance(n, int):
            raise NotImplementedError from None
        AnsiEscapeSequences.CURSOR_UP(n=n).execute()
        self.position -= (0, n)
        return self

    def down(self, n: int = 1) -> type[Cursor]:
        if not isinstance(n, int):
            raise NotImplementedError from None
        AnsiEscapeSequences.CURSOR_DOWN(n=n).execute()
        self.position += (0, n)
        return self

    def left(self, n: int = 1) -> type[Cursor]:
        if not isinstance(n, int):
            raise NotImplementedError from None
        AnsiEscapeSequences.CURSOR_LEFT(n=n).execute()
        self.position -= (n, 0)
        return self

    def right(self, n: int = 1) -> type[Cursor]:
        if not isinstance(n, int):
            raise NotImplementedError from None
        AnsiEscapeSequences.CURSOR_RIGHT(n=n).execute()
        self.position += (n, 0)
        return self

    def retreat(self) -> type[Cursor]:
        return self.go_to(Coordinate(0, self.position.y))

    def go_to(self, coordinate: Coordinate | tuple[int, int]) -> type[Cursor]:
        if not isinstance(coordinate, (Coordinate, tuple)):
            raise NotImplementedError from None
        elif isinstance(coordinate, tuple) and tuple(map(type, coordinate)) != (int, int):
            raise NotImplementedError from None
        coordinate = coordinate if isinstance(coordinate, Coordinate) else Coordinate(*coordinate)
        AnsiEscapeSequences.CURSOR_GO_TO(coordinate).execute()
        self.position = coordinate
        return self

    def sync_position(self) -> None:
        self.position = self.get_live_position()

    def show(self) -> type[Cursor]:
        AnsiEscapeSequences.CURSOR_VISIBILITY(on=True).execute()
        return self

    def hide(self) -> type[Cursor]:
        AnsiEscapeSequences.CURSOR_VISIBILITY(on=False).execute()
        return self

    def clear_line(self, *, before_cursor: bool = True, after_cursor: bool = True) -> type[Cursor]:
        if before_cursor and after_cursor:
            AnsiEscapeSequences.CLEAR_LINE.execute()
        elif before_cursor:
            AnsiEscapeSequences.CLEAR_LINE_LEFT.execute()
        elif after_cursor:
            AnsiEscapeSequences.CLEAR_LINE_RIGHT.execute()
        return self

    @contextmanager
    def in_position(self, position: Coordinate) -> Iterator[type[Cursor]]:
        old_position = self.position
        self.go_to(position)
        try:
            yield self
        finally:
            self.position = old_position

    def get_print_displacement(
            self, value: SupportsString) -> Generator[tuple[CharacterInfo, Coordinate], None, Coordinate]:
        text = Text.as_text(value)
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
        for character_info in text:
            yield character_info, Coordinate(width, height)
            if isinstance(character_info.character, AnsiEscapeSequence):
                displacement = character_info.character.cursor_print_displacement(self.position)
                if displacement.y and width > largest_width:
                    largest_width = width
                width += displacement.x
                height += displacement.y
            elif character_info.character == Characters.NEWLINE:
                if width > largest_width:
                    largest_width = width
                width = 0
                height += 1
            elif character_info.character == Characters.TAB:
                cursor_x = self.terminal.cursor.position.x + width
                width += int(ceil(cursor_x / 4)) * 4 - cursor_x
            elif character_info.character == Characters.BACKSPACE:
                width -= 1
            elif character_info.character == Characters.CARRIAGE_RETURN:
                width = 0
            elif category(character_info.character)[0] in "MC":
                pass
            else:
                width += east_asian_width_lookup[east_asian_width(character_info.character)]
        largest_width = width
        return Coordinate(max(width, largest_width), height)
