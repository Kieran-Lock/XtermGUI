from __future__ import annotations
from typing import Iterator
from dataclasses import dataclass, field
from math import sqrt


@dataclass(frozen=True, slots=True, order=True)
class Coordinate:
    sort_index: float = field(init=False, repr=False)
    x: int
    y: int

    def __post_init__(self) -> None:
        object.__setattr__(self, "sort_index", abs(self))

    def __add__(self, other: Coordinate | tuple[int, int]) -> Coordinate:
        if not isinstance(other, (Coordinate, tuple)):
            return NotImplemented
        elif isinstance(other, tuple) and tuple(map(type, other)) != (int, int):
            return NotImplemented
        x, y = (other.x, other.y) if isinstance(other, Coordinate) else (other[0], other[1])
        return Coordinate(self.x + x, self.y + y)

    def __sub__(self, other: Coordinate | tuple[int, int]) -> Coordinate:
        if not isinstance(other, (Coordinate, tuple)):
            return NotImplemented
        elif isinstance(other, tuple) and tuple(map(type, other)) != (int, int):
            return NotImplemented
        x, y = (other.x, other.y) if isinstance(other, Coordinate) else (other[0], other[1])
        return Coordinate(self.x - x, self.y - y)

    def __mul__(self, scalar: float) -> Coordinate:
        if not isinstance(scalar, (int, float)):
            return NotImplemented
        return Coordinate(round(self.x * scalar), round(self.y * scalar))

    def __div__(self, scalar: float) -> Coordinate:
        if not isinstance(scalar, (int, float)):
            return NotImplemented
        return Coordinate(round(self.x / scalar), round(self.y / scalar))

    def __floordiv__(self, scalar: float) -> Coordinate:
        if not isinstance(scalar, (int, float)):
            return NotImplemented
        return Coordinate(int(self.x // scalar), int(self.y // scalar))

    def __iter__(self) -> Iterator:
        return (self.x, self.y).__iter__()

    def __contains__(self, item: float) -> bool:
        return item in (self.x, self.y)

    def __abs__(self) -> float:
        return sqrt(self.x ** 2 + self.y ** 2)
