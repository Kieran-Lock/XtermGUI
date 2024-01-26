from enum import Enum
from typing import Callable

from .escape_sequence import AnsiEscapeSequence
from ..geometry import Coordinate


def boolean_escape_sequence(code: str) -> Callable[[bool], AnsiEscapeSequence]:
    def get_sequence(*, on: bool) -> AnsiEscapeSequence:
        return AnsiEscapeSequence(f"\033[?{code}{"h" if on else "l"}")

    return get_sequence


def scalar_escape_sequence(code: str) -> Callable[[int], AnsiEscapeSequence]:
    def get_sequence(*, n: int = 1) -> AnsiEscapeSequence:
        return AnsiEscapeSequence(f"\033[{n}{code}")

    return get_sequence


def coordinate_escape_sequence(code: str) -> Callable[[Coordinate], AnsiEscapeSequence]:
    def get_sequence(coordinate: Coordinate) -> AnsiEscapeSequence:
        return AnsiEscapeSequence(f"\033[{coordinate.y + 1};{coordinate.x + 1}{code}")

    return get_sequence


class AnsiEscapeSequences(Enum):
    END = AnsiEscapeSequence("\033[0m")
    REQUEST_LIVE_CURSOR_POSITION = AnsiEscapeSequence("\033[6n")
    CLEAR_LINE = AnsiEscapeSequence("\033[2K")
    CLEAR_LINE_LEFT = AnsiEscapeSequence("\033[1K")
    CLEAR_LINE_RIGHT = AnsiEscapeSequence("\033[K")
    SGR_MOUSE_REPORTING = boolean_escape_sequence("1006")
    LINE_WRAPPING = boolean_escape_sequence("7")
    CURSOR_VISIBILITY = boolean_escape_sequence("25")
    CURSOR_LEFT = scalar_escape_sequence("D")
    CURSOR_RIGHT = scalar_escape_sequence("C")
    CURSOR_UP = scalar_escape_sequence("A")
    CURSOR_DOWN = scalar_escape_sequence("B")
    CURSOR_GO_TO = coordinate_escape_sequence("H")
