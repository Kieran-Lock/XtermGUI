from __future__ import annotations
from dataclasses import dataclass, field


@dataclass(order=True, slots=True, frozen=True)
class Entry:
    value: int
    fixed: bool = field(default=False, compare=False)

    def is_empty(self) -> bool:
        return not self.value

    def __str__(self) -> str:
        return str(self.value)

    def __add__(self, value: int) -> Entry:
        if self.value == 9:
            return Entry(0)
        return Entry(self.value + value)

    def __sub__(self, value: int) -> Entry:
        if self.is_empty():
            return Entry(9)
        return Entry(self.value - value)

    def __rlshift__(self, other: int) -> int:
        return other << self.value
