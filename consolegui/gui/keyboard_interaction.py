from __future__ import annotations
from typing import Callable, TYPE_CHECKING
from dataclasses import dataclass, field
from ..input import KeyboardEvent, MouseEvent, Event
if TYPE_CHECKING:
    from .gui import GUI


@dataclass(frozen=True, slots=True)
class KeyboardInteraction:
    event: Event
    consequence: Callable[[GUI, KeyboardEvent], None] | None = field(default=None, init=False)

    def __call__(self, consequence: Callable[[GUI, KeyboardEvent], None]) -> KeyboardInteraction:
        object.__setattr__(self, "consequence", consequence)
        return self

    def matches_event(self, event: KeyboardEvent | MouseEvent) -> bool:
        if isinstance(event, MouseEvent):
            return False
        return self.event.trigger_condition(event)
