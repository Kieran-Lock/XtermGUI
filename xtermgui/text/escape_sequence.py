from __future__ import annotations

from dataclasses import dataclass, field
from functools import partial
from re import compile, finditer
from typing import NamedTuple, Callable, Literal

from ..geometry import Coordinate


class Match(NamedTuple):
    start: int
    end: int
    escape_sequence: AnsiEscapeSequence


@dataclass(frozen=True, slots=True)
class AnsiEscapeSequence(str):
    REGEX = compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")

    escape_sequence: str
    validate: bool = field(default=True, repr=False)
    _displacement_getter: Callable[[Coordinate], Coordinate] = field(init=False, default=None, repr=False)

    def __post_init__(self) -> None:
        if self.validate and not self.is_valid(self.escape_sequence):
            raise ValueError("Cannot create invalid ANSI escape sequence.") from None
        object.__setattr__(self, "_displacement_getter", self._get_expected_displacement_getter(self.escape_sequence))

    def __new__(cls, escape_sequence: str, _displacement_getter: Coordinate = Coordinate(0, 0),
                validate: bool = True):
        return super(AnsiEscapeSequence, cls).__new__(cls, escape_sequence)

    def __str__(self) -> str:
        return self.escape_sequence

    def __len__(self) -> Literal[1]:
        return 1

    @classmethod
    def is_valid(cls, escape_sequence: str) -> bool:
        return cls.REGEX.match(escape_sequence) is not None

    @classmethod
    def matches(cls, string: str) -> list[Match]:
        return [Match(*match.span(), cls(match.string[match.start(0):match.end(0)], validate=False)) for match in
                finditer(cls.REGEX, string)]  # TODO: Never gets the correct displacement getter

    def execute(self, flush: bool = True) -> None:
        print(self, end="", flush=flush)

    def cursor_print_displacement(self, cursor_position: Coordinate) -> Coordinate:
        return self._displacement_getter(cursor_position)

    @staticmethod
    def _get_expected_displacement_getter(escape_sequence: str) -> Coordinate:
        match list(escape_sequence):
            case "\033[H":
                return partial(lambda cursor_position: Coordinate(0, 0) - cursor_position)
            case ['\033', '[', x, ';', y, 'H' | 'f'] if x.isdigit() and y.isdigit():
                return partial(lambda cursor_position: Coordinate(int(x), int(y)) - cursor_position)
            case ['\033', '[', n, 'A'] if n.isdigit():
                return partial(lambda _: Coordinate(0, -int(n)))
            case ['\033', '[', n, 'B'] if n.isdigit():
                return partial(lambda _: Coordinate(0, int(n)))
            case ['\033', '[', n, 'C'] if n.isdigit():
                return partial(lambda _: Coordinate(int(n), 0))
            case ['\033', '[', n, 'D'] if n.isdigit():
                return partial(lambda _: Coordinate(-int(n), 0))
            case ['\033', '[', n, 'E'] if n.isdigit():
                return partial(lambda cursor_position: Coordinate(0, int(n)) - cursor_position)
            case ['\033', '[', n, 'F'] if n.isdigit():
                return partial(lambda cursor_position: Coordinate(0, -int(n)) - cursor_position)
            case ['\033', '[', n, 'G'] if n.isdigit():
                return partial(lambda cursor_position: Coordinate(cursor_position.x, int(n)) - cursor_position)
            case _:
                return partial(lambda _: Coordinate(0, 0))
