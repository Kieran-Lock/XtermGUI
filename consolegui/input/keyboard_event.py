from dataclasses import dataclass
from typing import ClassVar


@dataclass(frozen=True, slots=True)
class KeyboardEvent:
    UNRECOGNIZED: ClassVar[str] = "KEYBOARD_UNRECOGNIZED"
    ANY: ClassVar[str] = "KEYBOARD_ANY"
    name: str
