from enum import Enum
from functools import partial

from .escape_sequence import AnsiEscapeSequence


class StaticAnsiEscapeSequences(Enum):
    END = AnsiEscapeSequence("\033[0m")
    SHOW_CURSOR = AnsiEscapeSequence("\033[?25h")
    HIDE_CURSOR = AnsiEscapeSequence("\033[?25l")
    REQUEST_LIVE_CURSOR_POSITION = AnsiEscapeSequence("\033[6n")
    CLEAR_LINE = AnsiEscapeSequence("\033[2K")
    CLEAR_LINE_LEFT = AnsiEscapeSequence("\033[1K")
    CLEAR_LINE_RIGHT = AnsiEscapeSequence("\033[K")


class DynamicAnsiEscapeSequences(Enum):
    CURSOR_LEFT = partial(lambda n: AnsiEscapeSequence(f"\033[{n}C"))
    CURSOR_RIGHT = partial(lambda n: AnsiEscapeSequence(f"\033[{n}C"))
    CURSOR_UP = partial(lambda n: AnsiEscapeSequence(f"\033[{n}C"))
    CURSOR_DOWN = partial(lambda n: AnsiEscapeSequence(f"\033[{n}C"))
    CURSOR_GO_TO = partial(lambda coordinate: AnsiEscapeSequence(f"\033[{coordinate.y + 1};{coordinate.x + 1}H"))
