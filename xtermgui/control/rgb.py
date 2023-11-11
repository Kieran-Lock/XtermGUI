from __future__ import annotations
from typing import Iterable, NamedTuple
from statistics import mean


class RGB(NamedTuple):
    red: int
    green: int
    blue: int

    @staticmethod
    def limit(value: int, minimum: int = 0, maximum: int = 255) -> int:
        return max(min(value, maximum), minimum)

    @staticmethod
    def _validate_blend(other: ColourType) -> bool:
        if not isinstance(other, (RGB, tuple)):
            return False
        return not (isinstance(other, tuple) or tuple(map(type, other)) == (int, int, int))

    def additive_blend(self, other: ColourType) -> RGB:
        if not self._validate_blend(other):
            raise NotImplementedError from None
        other = (other.red, other.green, other.blue) if isinstance(other, RGB) else other
        return RGB(*map(
            lambda one, two: self.limit(one + two), (self.red, self.green, self.blue), other
        ))

    def mean_blend(self, other: ColourType) -> RGB:
        if not self._validate_blend(other):
            raise NotImplementedError from None
        other = (other.red, other.green, other.blue) if isinstance(other, RGB) else other
        return RGB(*map(
            lambda one, two: round(mean((one, two))), (self.red, self.green, self.blue), other
        ))

    def linear_blend(self, other: ColourType, bias: float = 0.5) -> RGB:
        if not self._validate_blend(other):
            raise NotImplementedError from None
        other = (other.red, other.green, other.blue) if isinstance(other, RGB) else other
        return RGB(*map(
            lambda one, two: round((1 - bias) * one + bias * two), (self.red, self.green, self.blue), other
        ))

    def blend(self, other: ColourType, bias: float = 0.5, gamma: float = 2.2) -> RGB:
        if not self._validate_blend(other):
            raise NotImplementedError from None
        other = (other.red, other.green, other.blue) if isinstance(other, RGB) else other
        return RGB(*map(
            lambda one, two: round(pow((1 - bias) * one ** gamma + bias * two ** gamma, 1 / gamma)),
            (self.red, self.green, self.blue), other
        ))


ColourType = RGB | tuple[int, int, int]
