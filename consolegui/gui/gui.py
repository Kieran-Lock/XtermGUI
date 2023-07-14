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
from ..control import Cursor, SupportsString
from ..input import read_console, console_inputs


@dataclass(slots=True)
class GUI:
    ERASE_CHARACTER: ClassVar[str] = " "
    is_running: bool = field(default=False, init=False)
    content: dict[Coordinate, SupportsString] = field(compare=False, init=False, default_factory=dict, repr=False)
    interactions: list[KeyboardInteraction | MouseInteraction] = field(default_factory=list, init=False)

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
    def start(self) -> Iterator[GUI]:
        def _start() -> None:
            with console_inputs():
                while self.is_running:
                    self.update()

        self.clear()
        thread = Thread(target=_start, daemon=True)
        self.is_running = True
        thread.start()

        try:
            yield self
        finally:
            self.is_running = False
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
        for interaction in self.interactions:
            if interaction.matches_event(event):
                interaction.consequence(self, event)

    def clear(self) -> None:
        system("clear")
        self.content = {}
