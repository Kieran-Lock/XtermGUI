from dataclasses import dataclass
from typing import ClassVar
from ..geometry import Coordinate


@dataclass(frozen=True, slots=True)
class MouseEvent:
    UNRECOGNIZED: ClassVar[str] = "MOUSE_UNRECOGNIZED"
    ANY: ClassVar[str] = "MOUSE_ANY"
    name: str
    coordinate: Coordinate
