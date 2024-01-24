from __future__ import annotations

from contextlib import contextmanager
from dataclasses import dataclass, field
from inspect import getmembers
from os import system
from typing import ClassVar, Iterator
from sys import stdout

from ..control import Cursor, Text
from ..geometry import Coordinate
from ..input import Events, KeyboardEvent, read_console
from ..utilities import KillableThread, SupportsString, console_inputs
from .input_state import InputState
from .keyboard_interaction import KeyboardInteraction
from .mouse_interaction import MouseInteraction


@dataclass(slots=True)
class GUI:
    ERASE_CHARACTER: ClassVar[str] = ' '
    is_running: bool = field(default=False, init=False)
    content: dict[Coordinate, SupportsString] = field(compare=False, init=False, default_factory=dict, repr=False)
    interactions: list[KeyboardInteraction | MouseInteraction] = field(default_factory=list, init=False)
    input_state: InputState = field(compare=False, init=False, default_factory=InputState, repr=False)

    def __post_init__(self) -> None:
        self.interactions = [interaction for interaction in self.get_interactions()]

    def get_interactions(self) -> Iterator[KeyboardInteraction, MouseInteraction]:
        return (interaction[1] for interaction in getmembers(
            self.__class__, predicate=lambda member: isinstance(member, (MouseInteraction, KeyboardInteraction))
        ))

    def print(self, *text: SupportsString, sep: SupportsString = ' ', end: SupportsString = "", flush: bool = True, at: Coordinate | None = None) -> None:
        if at is not None:
            Cursor.go_to(at)
        print(*text, sep=str(sep), end=str(end), flush=flush)
        for character in str(sep).join(map(str, text)) + str(end):
            self.content[Cursor.position] = character
            Cursor.update_position_on_print(character)

    def maintain_indent_print(self, *text: SupportsString, sep: SupportsString = ' ', end: SupportsString = "", flush: bool = True, at: Coordinate | None = None):
        if at is not None:
            Cursor.go_to(at)
        result = str(sep).join(map(str, text)) + str(end)
        initial_x = Cursor.position.x
        for i, string in enumerate(result.split('\n')):
            y = Cursor.position.y + 1 if i else Cursor.position.y
            self.print(string, flush=False, at=Coordinate(initial_x, y))
        if flush:
            stdout.flush()

    def erase(self, at: Coordinate | None = None, flush: bool = True) -> None:
        if at is not None:
            Cursor.go_to(at)
        print(self.__class__.ERASE_CHARACTER, end="", flush=flush)
        self.content[Cursor.position] = self.__class__.ERASE_CHARACTER
        Cursor.update_position_on_print(self.__class__.ERASE_CHARACTER)

    @contextmanager
    def start(self, inputs: bool = True) -> Iterator[GUI]:
        self.is_running = True
        try:
            if inputs:
                def _start() -> None:
                    while self.is_running:
                        self.update()
                thread = KillableThread(target=_start, daemon=True)
                with console_inputs():
                    thread.start()
                    try:
                        yield self
                    finally:
                        thread.kill()
            else:
                yield self
        finally:
            self.is_running = False
            Cursor.go_to(Coordinate(0, self.get_size().y + 2))

    def get_size(self) -> Coordinate:
        if not self.content:
            return Coordinate(0, 0)
        x = max(self.content, key=lambda coordinate: coordinate.x).x
        y = max(self.content, key=lambda coordinate: coordinate.y).y
        return Coordinate(x, y)

    def update(self) -> None:
        event = read_console()
        if self.input_state.is_inputting:
            if self.keyboard_prompt_input_interaction.matches_event(event):
                self.keyboard_prompt_input_interaction.consequence(self, event)
            return
        for interaction in self.interactions:
            if interaction.matches_event(event):
                interaction.consequence(self, event)

    def clear(self) -> None:
        system("clear")
        self.content = {}

    def input(self, *prompt: SupportsString, sep: SupportsString = ' ', end: SupportsString = "", flush: bool = True, at: Coordinate | None = None, after: SupportsString = "", echo: SupportsString = None) -> str:
        self.print(*prompt, sep=sep, end=end, flush=flush, at=at)
        with self.input_state.inputting(echo):
            if after:
                self.print(after)
        return self.input_state.flush_buffer()

    @KeyboardInteraction(Events.ANY_KEYBOARD.value)
    def keyboard_prompt_input_interaction(self, event: KeyboardEvent) -> None:
        if event == Events.ENTER.value:
            return self.input_state.end_input()
        if event == Events.BACKSPACE.value:
            if not self.input_state.pop_from_buffer():
                return
            if self.input_state.tabs_involved_in_display():  # TODO: Efficiency improvement by tracking position of first tab
                Cursor.go_to(self.input_state.position_of_input_start)
                Cursor.clear_line(before_cursor=False)
                replacement = self.input_state.displayed_text
                self.print(replacement)
                return
            Cursor.left()
            self.erase()
            Cursor.left()
            return
        input_name_mapping = {
            Events.TAB.value.name: Text.TAB,
            Events.POUND.value.name: "£",
        }
        print_character = self.input_state.append_to_buffer(input_name_mapping.get(event.name, event.name))
        self.print(print_character)
