from __future__ import annotations
from typing import Callable, TYPE_CHECKING
from dataclasses import dataclass, field
from ..input import KeyboardEvent, MouseEvent, Event
from ..geometry import Region
if TYPE_CHECKING:
    from .gui import GUI


@dataclass(frozen=True, slots=True)
class MouseInteraction:
    event: Event
    region: Region
    consequence: Callable[[GUI, MouseEvent], None] | None = field(default=None, init=False)

    def __call__(self, consequence: Callable[[GUI, MouseEvent], None]) -> MouseInteraction:
        object.__setattr__(self, "consequence", consequence)
        return self

    def matches_event(self, event: KeyboardEvent | MouseEvent) -> bool:
        if isinstance(event, KeyboardEvent):
            return False
        return self.event.trigger_condition(event) and event.coordinate in self.region
