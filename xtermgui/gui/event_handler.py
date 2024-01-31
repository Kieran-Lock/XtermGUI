from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Callable, TYPE_CHECKING, Self, cast

from ..geometry import Region
from ..input import InputEvent, MouseEvent

if TYPE_CHECKING:
    from .gui import GUI


@dataclass(frozen=True, slots=True)
class EventHandler(ABC):
    matcher: Callable[[GUI, InputEvent], bool]
    _handler: Callable[[GUI, InputEvent], None] | None = field(default=None, init=False)

    def __call__(self, handler: Callable[[GUI, InputEvent], None]) -> Self:
        object.__setattr__(self, "_handler", handler)
        return self

    @abstractmethod
    def matches(self, gui: GUI, event: InputEvent) -> bool:
        ...

    def handle(self, gui: GUI, event: InputEvent) -> bool:
        if self.matches(gui, event):
            self._handler(gui, event)
            return True
        return False

    @classmethod
    @abstractmethod
    def default(cls, event: str) -> EventHandler:
        ...


@dataclass(frozen=True, slots=True)
class KeyboardEventHandler(EventHandler):
    def matches(self, gui: GUI, event: InputEvent) -> bool:
        return event.is_keyboard and self.matcher(gui, event)

    @classmethod
    def default(cls, event: str) -> KeyboardEventHandler:
        return cls(lambda _, input_event: event == input_event.event)


@dataclass(frozen=True, slots=True)
class MouseEventHandler(EventHandler):
    region: Region | None = None

    def matches(self, gui: GUI, event: InputEvent) -> bool:
        if event.is_keyboard:
            return False
        is_in_region = True if self.region is None else cast(MouseEvent, event).coordinate in self.region
        return is_in_region and self.matcher(gui, event)

    @classmethod
    def default(cls, event: str, region: Region | None = None) -> MouseEventHandler:
        return cls(lambda _, input_event: event == input_event.event, region=region)

    def scoped_to(self, region: Region) -> MouseEventHandler:
        return MouseEventHandler(
            self.matcher,
            region=region,
        )
