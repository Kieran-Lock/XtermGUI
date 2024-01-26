from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, TYPE_CHECKING, Self

from ..geometry import Region
from ..input import KeyboardEvent, MouseEvent, Event

if TYPE_CHECKING:
    from .gui import GUI


@dataclass(frozen=True, slots=True)
class MouseInteraction:
    event: Event
    region: Region | None = None
    consequence: Callable[[GUI, MouseEvent], None] | None = field(default=None, init=False)

    def __call__(self, consequence: Callable[[GUI, MouseEvent], None]) -> Self:
        object.__setattr__(self, "consequence", consequence)
        return self

    def matches_event(self, event: KeyboardEvent | MouseEvent) -> bool:
        if isinstance(event, KeyboardEvent):
            return False
        passed_region_check = True if self.region is None else event.coordinate in self.region
        return self.event.trigger_condition(event) and passed_region_check
