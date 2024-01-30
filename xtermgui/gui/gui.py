from __future__ import annotations

from contextlib import contextmanager
from dataclasses import dataclass, field
from inspect import getmembers
from os import system
from sys import stdout
from typing import ClassVar, Iterator, Self

from .event_handler import EventHandler, KeyboardEventHandler
from .input_state import InputState
from ..geometry import Coordinate
from ..input import KeyboardEvent, read_event, KeyboardCode
from ..terminal import terminal
from ..text import Text, Characters
from ..utilities import WorkerProcess, SupportsString


@dataclass(slots=True)
class GUI:
    INPUT_LOCK_PRIORITY: ClassVar[float | None] = None
    ERASE_CHARACTER: ClassVar[str] = ' '
    is_running: bool = field(default=False, init=False)
    content: dict[Coordinate, SupportsString] = field(compare=False, init=False, default_factory=dict, repr=False)
    event_handlers: list[EventHandler] = field(default_factory=list, init=False)
    input_state: InputState = field(compare=False, init=False, default_factory=InputState, repr=False)

    def __post_init__(self) -> None:
        self.event_handlers = [event_handler for event_handler in self.get_event_handlers()]

    def get_event_handlers(self) -> Iterator[EventHandler]:
        return (event_handler[1] for event_handler in getmembers(
            self.__class__, predicate=lambda member: isinstance(member, EventHandler)
        ))

    def print(self, *values: SupportsString, sep: SupportsString = ' ', end: SupportsString = "", flush: bool = True,
              at: Coordinate | None = None) -> None:
        if at is not None:
            terminal.cursor.go_to(at)
        text = Text.as_printed(*values, sep=sep, end=end, flush=flush, do_print=True)
        for character, cursor_position in terminal.cursor.get_print_displacement(text):
            self.content[cursor_position] = character
        terminal.cursor.sync_position()

    def print_inline(self, *values: SupportsString, sep: SupportsString = ' ', end: SupportsString = "",
                     flush: bool = True, at: Coordinate | None = None) -> None:
        if at is not None:
            terminal.cursor.go_to(at)
        result = str(sep).join(map(str, values)) + str(end)
        initial_x = terminal.cursor.position.x
        for i, string in enumerate(result.split('\n')):
            y = terminal.cursor.position.y + 1 if i else terminal.cursor.position.y
            self.print(string, flush=False, at=Coordinate(initial_x, y))
        if flush:
            stdout.flush()

    def erase(self, at: Coordinate | None = None, flush: bool = True) -> None:
        if at is not None:
            terminal.cursor.go_to(at)
        print(self.ERASE_CHARACTER, end="", flush=flush)
        self.content[terminal.cursor.position] = self.ERASE_CHARACTER
        terminal.cursor.sync_position()

    @contextmanager
    def start(self, inputs: bool = True) -> Iterator[Self]:
        self.is_running = True
        try:
            if inputs:
                def _start() -> None:
                    while self.is_running:
                        self.update()

                process = WorkerProcess(target=_start, daemon=True)
                with terminal.setup_inputs():
                    process.start()
                    try:
                        yield self
                    finally:
                        process.kill()
            else:
                yield self
        finally:
            self.is_running = False
            terminal.cursor.go_to(Coordinate(0, self.get_size().y + 2))

    def get_size(self) -> Coordinate:
        if not self.content:
            return Coordinate(0, 0)
        return Coordinate(
            max(coordinate.x for coordinate in self.content),
            max(coordinate.y for coordinate in self.content),
        )

    def update(self) -> None:
        try:
            event = read_event()
        except ValueError:  # Stdin closed
            return
        if self.input_state.is_inputting:
            self.keyboard_prompt_input_event_handler.handle(self, event)
            return
        for handler in self.event_handlers:
            handler.handle(self, event)

    def clear(self) -> None:
        system("clear")
        self.content = {}

    def input(self, *prompt: SupportsString, sep: SupportsString = ' ', end: SupportsString = "", flush: bool = True,
              at: Coordinate | None = None, after: SupportsString = "", echo: SupportsString = None) -> str:
        self.print(*prompt, sep=sep, end=end, flush=flush, at=at)
        with self.input_state.inputting(echo):
            if after:
                self.print(after)
        return self.input_state.flush_buffer()

    @KeyboardEventHandler(lambda gui, _: gui.input_state.is_inputting)
    def keyboard_prompt_input_event_handler(self, event: KeyboardEvent) -> None:
        if not self.input_state.is_inputting:
            return
        if event == KeyboardCode.ENTER:
            return self.input_state.end_input()
        if event == KeyboardCode.BACKSPACE:
            if not self.input_state.pop_from_buffer():
                return
            if self.input_state.tabs_involved_in_display():  # TODO: Try tracking position of first tab for efficiency
                terminal.cursor.go_to(self.input_state.position_of_input_start)  # TODO: Consider cursor position saving
                terminal.cursor.clear_line(before_cursor=False)
                replacement = self.input_state.displayed_text
                self.print(replacement)
                return
            terminal.cursor.left()
            self.erase()
            terminal.cursor.left()
            return
        input_name_mapping = {
            KeyboardCode.TAB: Characters.TAB,
            KeyboardCode.POUND: '£',
        }
        print_character = self.input_state.append_to_buffer(input_name_mapping.get(event.event, event.event))
        self.print(print_character)
