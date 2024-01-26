from __future__ import annotations

from dataclasses import dataclass, field
from math import sqrt
from typing import Iterator


@dataclass(frozen=True, slots=True, order=True)
class Coordinate:
    sort_index: float = field(init=False, repr=False)
    x: int
    y: int

    def __post_init__(self) -> None:
        object.__setattr__(self, "sort_index", abs(self))

    def __add__(self, other: Coordinate | tuple[int, int]) -> Coordinate:
        if not isinstance(other, (Coordinate, tuple)):
            raise NotImplementedError from None
        elif isinstance(other, tuple) and tuple(map(type, other)) != (int, int):
            raise NotImplementedError from None
        x, y = (other.x, other.y) if isinstance(other, Coordinate) else (other[0], other[1])
        return Coordinate(self.x + x, self.y + y)

    def __sub__(self, other: Coordinate | tuple[int, int]) -> Coordinate:
        if not isinstance(other, (Coordinate, tuple)):
            raise NotImplementedError from None
        elif isinstance(other, tuple) and tuple(map(type, other)) != (int, int):
            raise NotImplementedError from None
        x, y = (other.x, other.y) if isinstance(other, Coordinate) else (other[0], other[1])
        return Coordinate(self.x - x, self.y - y)

    def __mul__(self, scalar: float) -> Coordinate:
        if not isinstance(scalar, (int, float)):
            raise NotImplementedError from None
        return Coordinate(round(self.x * scalar), round(self.y * scalar))

    def __div__(self, scalar: float) -> Coordinate:
        if not isinstance(scalar, (int, float)):
            raise NotImplementedError from None
        return Coordinate(round(self.x / scalar), round(self.y / scalar))

    def __floordiv__(self, scalar: float) -> Coordinate:
        if not isinstance(scalar, (int, float)):
            raise NotImplementedError from None
        return Coordinate(int(self.x // scalar), int(self.y // scalar))

    def __iter__(self) -> Iterator:
        return (self.x, self.y).__iter__()

    def __contains__(self, item: float) -> bool:
        return item in (self.x, self.y)

    def __abs__(self) -> float:
        return sqrt(self.x ** 2 + self.y ** 2)

    def __bool__(self) -> bool:
        return bool(self.x or self.y)
