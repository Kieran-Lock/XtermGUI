from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any

from ..geometry import Coordinate


@dataclass(frozen=True, slots=True, kw_only=True)
class InputEvent(ABC):
    event: str

    @classmethod
    @abstractmethod
    def unrecognized(cls, *args: Any) -> InputEvent:
        ...

    @property
    @abstractmethod
    def is_keyboard(self) -> bool:
        ...


@dataclass(frozen=True, slots=True, kw_only=True)
class KeyboardEvent(InputEvent):
    UNRECOGNIZED_NAME = "UNRECOGNIZED_KEYBOARD"

    @classmethod
    def unrecognized(cls) -> KeyboardEvent:
        return cls(event=cls.UNRECOGNIZED_NAME)

    @property
    def is_keyboard(self) -> bool:
        return True


@dataclass(frozen=True, slots=True, kw_only=True)
class MouseEvent(InputEvent):
    UNRECOGNIZED_NAME = "UNRECOGNIZED_MOUSE"

    coordinate: Coordinate

    @classmethod
    def unrecognized(cls, *, coordinate) -> MouseEvent:
        return cls(event=cls.UNRECOGNIZED_NAME, coordinate=coordinate)

    @property
    def is_keyboard(self) -> bool:
        return False
