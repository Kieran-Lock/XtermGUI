from enum import Enum
from functools import partial
from typing import Callable

from .escape_sequence import AnsiEscapeSequence
from ..geometry import Coordinate


def boolean_escape_sequence(code: str) -> Callable[[bool], AnsiEscapeSequence]:
    def get_sequence(*, on: bool) -> AnsiEscapeSequence:
        return AnsiEscapeSequence(f"\033[?{code}{"h" if on else "l"}")

    return partial(get_sequence)


def scalar_cursor_escape_sequence(code: str) -> Callable[[int], AnsiEscapeSequence]:
    def get_sequence(n: int = 1) -> AnsiEscapeSequence:
        return AnsiEscapeSequence(f"\033[{n}{code}")

    return partial(get_sequence)


def coordinate_escape_sequence(
        code: str, formatter: Callable[[Coordinate], str]) -> Callable[[Coordinate], AnsiEscapeSequence]:
    def get_sequence(coordinate: Coordinate) -> AnsiEscapeSequence:
        return AnsiEscapeSequence(f"\033[{formatter(coordinate)}{code}")

    return partial(get_sequence)


def constant_escape_sequence(code: str) -> AnsiEscapeSequence:
    return AnsiEscapeSequence(f"\033[{code}")


class AnsiEscapeSequences(Enum):
    END = constant_escape_sequence("0m")
    REQUEST_LIVE_CURSOR_POSITION = constant_escape_sequence("6n")
    CLEAR_LINE = constant_escape_sequence("2K")
    CLEAR_LINE_LEFT = constant_escape_sequence("1K")
    CLEAR_LINE_RIGHT = constant_escape_sequence("K")
    SGR_MOUSE_REPORTING = boolean_escape_sequence("1006")
    LINE_WRAPPING = boolean_escape_sequence("7")
    CURSOR_VISIBILITY = boolean_escape_sequence("25")
    CURSOR_HOME = constant_escape_sequence("H")
    CURSOR_GO_TO = coordinate_escape_sequence("H", lambda coordinate: f"{coordinate.y + 1};{coordinate.x + 1}")
    CURSOR_LEFT = scalar_cursor_escape_sequence("D")
    CURSOR_RIGHT = scalar_cursor_escape_sequence("C")
    CURSOR_UP = scalar_cursor_escape_sequence("A")
    CURSOR_DOWN = scalar_cursor_escape_sequence("B")
    CURSOR_UP_RETREAT = scalar_cursor_escape_sequence("F")
    CURSOR_DOWN_RETREAT = scalar_cursor_escape_sequence("E")
    CURSOR_TO_COLUMN = scalar_cursor_escape_sequence("G")
