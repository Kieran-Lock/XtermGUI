from dataclasses import dataclass, field
from contextlib import contextmanager
from typing import Iterator
from ..geometry import Coordinate
from ..control import Cursor, Text
from ..utilities import SupportsString


@dataclass(slots=True)
class InputState:
    is_inputting: bool = field(default=False, init=False)
    buffer: str = field(default="", init=False)
    buffer_length: int = field(default=0, init=False, repr=False)
    tabs_in_input_buffer: int = field(default=0, init=False, repr=False)
    position_of_input_start: Coordinate | None = field(default=None, init=False)
    echo_character: SupportsString | None = field(default=None, init=False)

    @contextmanager
    def inputting(self, input_echo_character: SupportsString | None) -> Iterator[None]:
        if self.buffer:
            raise ValueError("Buffer is not empty. Flush the buffer before starting a new input.") from None
        self.position_of_input_start = Cursor.position
        self.echo_character = input_echo_character
        self.is_inputting = True
        Cursor.show()
        while self.is_inputting:
            pass
        Cursor.hide()
        try:
            yield
        finally:
            self.tabs_in_input_buffer = 0
    
    def end_input(self) -> None:
        self.is_inputting = False
    
    def flush_buffer(self) -> str:
        buffer = self.buffer
        self.buffer = ""
        return buffer

    def append_to_buffer(self, character: str) -> str:
        if character == Text.TAB:
            self.tabs_in_input_buffer += 1
        self.buffer += character
        self.buffer_length += 1
        return character if self.echo_character is None else self.echo_character
    
    def pop_from_buffer(self) -> str | None:
        if not self.buffer_length:
            return
        self.buffer, last = self.buffer[:-1], self.buffer[-1]
        self.buffer_length -= 1
        return last
    
    def tabs_involved_in_display(self) -> bool:
        return Text.TAB in self.echo_character or (self.tabs_in_input_buffer and self.echo_character is None)
    
    @property
    def displayed_text(self) -> str:
        return self.buffer if self.echo_character is None else self.echo_character * self.buffer_length
