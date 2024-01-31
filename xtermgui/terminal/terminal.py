from contextlib import contextmanager
from dataclasses import dataclass, field
from sys import stdin
from termios import tcgetattr, tcsetattr, ECHO, ICANON, TCSANOW, TCSADRAIN
from typing import Iterator

from .cursor import Cursor
from ..text import AnsiEscapeSequences
from ..utilities import Singleton


@dataclass(slots=True)
class Terminal(metaclass=Singleton):
    is_setup: bool = field(init=False, default=False)
    cursor: Cursor = field(init=False, default=None)

    def __post_init__(self) -> None:
        self.cursor = Cursor(self)
        self.cursor.position = self.cursor.get_live_position()

    @contextmanager
    def setup_inputs(self) -> Iterator[None]:
        if self.is_setup:
            yield
            return
        AnsiEscapeSequences.LINE_WRAPPING(on=False).execute()
        self.cursor.hide()
        AnsiEscapeSequences.NORMAL_MOUSE_REPORTING(on=True).execute()
        AnsiEscapeSequences.SGR_MOUSE_REPORTING(on=True).execute()
        with self.flags(ECHO, ICANON, set_method=TCSADRAIN):
            self.is_setup = True
            try:
                yield
            finally:
                self.is_setup = False
                AnsiEscapeSequences.SGR_MOUSE_REPORTING(on=False).execute()
                AnsiEscapeSequences.NORMAL_MOUSE_REPORTING(on=False).execute()
                self.cursor.show()
                AnsiEscapeSequences.LINE_WRAPPING(on=False).execute()

    @contextmanager
    def flags(self, *flags: int, set_method: int = TCSANOW) -> Iterator[None]:
        original_state = tcgetattr(stdin)
        new_state = original_state[:]
        new_state[3] -= sum(flags)
        tcsetattr(stdin, set_method, new_state)
        try:
            yield
        finally:
            tcsetattr(stdin, set_method, original_state)


terminal = Terminal()
