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
    interactions: list[KeyboardInteraction | MouseInteraction] = field(default_factory=list, init=False)

    def __post_init__(self) -> None:
        self.interactions = [interaction for interaction in self.get_interactions()]

    def get_interactions(self) -> Iterator[KeyboardInteraction, MouseInteraction]:
        return (interaction[1] for interaction in getmembers(
            self.__class__, predicate=lambda member: isinstance(member, (MouseInteraction, KeyboardInteraction))
        ))

    @staticmethod
    def print(text: SupportsString, at: Coordinate | None = None) -> None:
        if at is not None:
            Cursor.go_to(at)
        print(text, end="", flush=True)
        for character in str(text):
            Cursor.update_position_on_print(character)

    def erase(self, at: Coordinate | None = None) -> None:
        if at is not None:
            Cursor.go_to(at)
        print(self.__class__.ERASE_CHARACTER, end="", flush=True)
        Cursor.update_position_on_print(self.__class__.ERASE_CHARACTER)

    @contextmanager
    def start(self) -> Iterator[GUI]:
        def _start() -> None:
            with console_inputs():
                while self.is_running:
                    self.update()

        self.clear()
        thread = Thread(target=_start)
        self.is_running = True
        thread.start()

        try:
            yield self
        finally:
            self.is_running = False
            thread.join()
            Cursor.go_to(Coordinate(0, self.get_size().y))

    def get_size(self) -> Coordinate:
        return Coordinate(0, 0)

    def update(self) -> None:
        event = read_console()
        for interaction in self.interactions:
            if interaction.matches_event(event):
                interaction.consequence(self, event)

    @staticmethod
    def clear() -> None:
        system("clear")
