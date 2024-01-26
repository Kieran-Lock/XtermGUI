from contextlib import contextmanager
from sys import stdin
from termios import tcgetattr, tcsetattr, ECHO, ICANON, TCSADRAIN
from typing import Iterator

from ..cursor import Cursor
from ..text import AnsiEscapeSequences


class State:
    IS_SETUP: bool = False


@contextmanager
def terminal_inputs() -> Iterator[None]:
    if State.IS_SETUP:
        yield
        return
    original_state = tcgetattr(stdin)
    new_state = original_state[:]
    AnsiEscapeSequences.LINE_WRAPPING.value(on=False).execute()
    Cursor.hide()
    AnsiEscapeSequences.SGR_MOUSE_REPORTING.value(on=True).execute()
    new_state[3] -= (ECHO + ICANON)
    tcsetattr(stdin, TCSADRAIN, new_state)
    State.IS_SETUP = True
    try:
        yield
    finally:
        State.IS_SETUP = False
        tcsetattr(stdin, TCSADRAIN, original_state)  # Enable ECHO and ICANON
        AnsiEscapeSequences.LINE_WRAPPING.value(on=False).execute()
        Cursor.hide()
        AnsiEscapeSequences.SGR_MOUSE_REPORTING.value(on=True).execute()
