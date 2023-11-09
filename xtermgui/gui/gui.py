from __future__ import annotations
from contextlib import contextmanager
from threading import Thread
from dataclasses import dataclass, field
from inspect import getmembers
from typing import Iterator, ClassVar
from os import system
from .keyboard_interaction import KeyboardInteraction
from .mouse_interaction import MouseInteraction
from ..geometry import Coordinate
from ..control import Cursor, SupportsString, Text
from ..input import read_console, console_inputs, Events, KeyboardEvent


@dataclass(slots=True)
class GUI:
    ERASE_CHARACTER: ClassVar[str] = ' '
    is_running: bool = field(default=False, init=False)
    content: dict[Coordinate, SupportsString] = field(compare=False, init=False, default_factory=dict, repr=False)
    interactions: list[KeyboardInteraction | MouseInteraction] = field(default_factory=list, init=False)
    input_buffer: str = field(default="", init=False, repr=False, compare=False)
    is_input_mode: bool = field(default=False, init=False, repr=False, compare=False)
    input_cursor_position_stamp: Coordinate | None = field(default=None, init=False, repr=False, compare=False)
    input_echo: SupportsString = field(default=None, init=False, repr=False, compare=False)
    tabs_in_input_buffer: int = field(default=0, init=False, repr=False, compare=False)

    def __post_init__(self) -> None:
        self.interactions = [interaction for interaction in self.get_interactions()]

    def get_interactions(self) -> Iterator[KeyboardInteraction, MouseInteraction]:
        return (interaction[1] for interaction in getmembers(
            self.__class__, predicate=lambda member: isinstance(member, (MouseInteraction, KeyboardInteraction))
        ))

    def print(self, *text: SupportsString, sep: SupportsString = " ", end: SupportsString = "", flush: bool = True, at: Coordinate | None = None) -> None:
        if at is not None:
            Cursor.go_to(at)
        print(*text, sep=str(sep), end=str(end), flush=flush)
        for character in str(sep).join(map(str, text)) + str(end):
            self.content[Cursor.position] = character
            Cursor.update_position_on_print(character)

    def erase(self, at: Coordinate | None = None, flush: bool = True) -> None:
        if at is not None:
            Cursor.go_to(at)
        print(self.__class__.ERASE_CHARACTER, end="", flush=flush)
        self.content[Cursor.position] = self.__class__.ERASE_CHARACTER
        Cursor.update_position_on_print(self.__class__.ERASE_CHARACTER)

    @contextmanager
    def start(self, inputs: bool = False) -> Iterator[GUI]:
        def _start() -> None:
            with console_inputs():
                while self.is_running:
                    self.update()

        self.clear()
        self.is_running = True
        if inputs:
            thread = Thread(target=_start, daemon=True)
            thread.start()
        else:
            thread = None

        try:
            yield self
        finally:
            self.is_running = False
            if inputs:
                thread.join()
            Cursor.go_to(Coordinate(0, self.get_size().y + 2))

    def get_size(self) -> Coordinate:
        if not self.content:
            return Coordinate(0, 0)
        x = max(self.content, key=lambda coordinate: coordinate.x).x
        y = max(self.content, key=lambda coordinate: coordinate.y).y
        return Coordinate(x, y)

    def update(self) -> None:
        event = read_console()
        if self.is_input_mode:
            if self.keyboard_prompt_input_interaction.matches_event(event):
                self.keyboard_prompt_input_interaction.consequence(self, event)
            return
        for interaction in self.interactions:
            if interaction.matches_event(event):
                interaction.consequence(self, event)

    def clear(self) -> None:
        system("clear")
        self.content = {}
    
    def input(self, *prompt: SupportsString, sep: SupportsString = " ", end: SupportsString = "", flush: bool = True, at: Coordinate | None = None, after: SupportsString = "", echo: SupportsString = None) -> str:
        self.print(*prompt, sep=sep, end=end, flush=flush, at=at)
        self.input_cursor_position_stamp = Cursor.position
        self.input_echo = echo
        self.is_input_mode = True
        Cursor.show()
        while self.is_input_mode:
            pass
        Cursor.hide()
        if after:
            self.print(after)
        buffer = self.input_buffer
        self.input_buffer = ""
        self.tabs_in_input_buffer = 0
        return buffer
    
    @KeyboardInteraction(Events.ANY_KEYBOARD.value)
    def keyboard_prompt_input_interaction(self, event: KeyboardEvent) -> None:
        if event == Events.ENTER.value:
            self.is_input_mode = False
            return
        INPUT_NAME_MAPPING = {
            Events.TAB.value.name: Text.TAB,
            Events.POUND.value.name: "£",
        }

        if event == Events.BACKSPACE.value:
            if not self.input_buffer:
                return
            self.input_buffer = self.input_buffer[:-1]
            if Text.TAB in self.input_echo or (self.tabs_in_input_buffer and self.input_echo is None):  # TODO: Efficiency improvement by tracking position of first tab
                Cursor.go_to(self.input_cursor_position_stamp)
                Cursor.clear_line(before_cursor=False)
                replacement = self.input_buffer if self.input_echo is None else self.input_echo * len(self.input_buffer)
                self.print(replacement, at=self.input_cursor_position_stamp)
                return
            Cursor.left()
            self.erase()
            Cursor.left()
            return
        if event == Events.TAB.value:
            self.tabs_in_input_buffer += 1
        character = INPUT_NAME_MAPPING.get(event.name, event.name)
        self.print(character if self.input_echo is None else self.input_echo)
        self.input_buffer += character
