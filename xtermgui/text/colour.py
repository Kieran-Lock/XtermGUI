from __future__ import annotations

from statistics import mean
from typing import NamedTuple


class Colour(NamedTuple):
    red: int
    green: int
    blue: int

    @staticmethod
    def limit(value: int, minimum: int = 0, maximum: int = 255) -> int:
        return max(min(value, maximum), minimum)

    def additive_blend(self, other: ColourType) -> Colour:
        other = (other.red, other.green, other.blue) if isinstance(other, Colour) else other
        return Colour(*map(
            lambda one, two: self.limit(one + two), (self.red, self.green, self.blue), other
        ))

    def mean_blend(self, other: ColourType) -> Colour:
        other = (other.red, other.green, other.blue) if isinstance(other, Colour) else other
        return Colour(*map(
            lambda one, two: round(mean((one, two))), (self.red, self.green, self.blue), other
        ))

    def linear_blend(self, other: ColourType, bias: float = 0.5) -> Colour:
        other = (other.red, other.green, other.blue) if isinstance(other, Colour) else other
        return Colour(*map(
            lambda one, two: round((1 - bias) * one + bias * two), (self.red, self.green, self.blue), other
        ))

    def blend(self, other: ColourType, bias: float = 0.5, gamma: float = 2.2) -> Colour:
        other = (other.red, other.green, other.blue) if isinstance(other, Colour) else other
        return Colour(*map(
            lambda one, two: round(pow((1 - bias) * one ** gamma + bias * two ** gamma, 1 / gamma)),
            (self.red, self.green, self.blue), other
        ))


ColourType = Colour | tuple[int, int, int]
