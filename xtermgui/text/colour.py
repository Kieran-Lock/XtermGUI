from __future__ import annotations

from dataclasses import dataclass
from functools import cached_property
from typing import ClassVar

from .rgb import RGB
from .rgbs import RGBs


@dataclass(frozen=True, init=False)
class Colour:
    DEFAULT_BACKGROUND: ClassVar[RGB] = RGBs.DEFAULT_BACKGROUND_WSL.value

    foreground: RGB | tuple[int, int, int] | None = None
    background: RGB | tuple[int, int, int] | None = None

    def __init__(self, foreground: RGB | tuple[int, int, int] | None = None,
                 background: RGB | tuple[int, int, int] | None = None) -> None:
        foreground = RGBs.DEFAULT_FOREGROUND.value if foreground is None else foreground
        background = self.DEFAULT_BACKGROUND if background is None else background
        foreground = foreground if isinstance(foreground, RGB) else RGB(*foreground)
        background = background if isinstance(background, RGB) else RGB(*background)
        object.__setattr__(self, "foreground", foreground)
        object.__setattr__(self, "background", background)

    @classmethod
    def configure_default_background(cls, rgb: RGB) -> RGB:
        cls.DEFAULT_BACKGROUND = rgb
        return cls.DEFAULT_BACKGROUND

    def __add__(self, other: Colour) -> Colour:
        if not isinstance(other, Colour):
            raise NotImplementedError from None
        foreground = self.foreground if self.has_foreground else other.foreground
        background = self.background if self.has_background else other.background
        return Colour(foreground=foreground, background=background)

    def __sub__(self, other: Colour) -> Colour:
        if not isinstance(other, Colour):
            raise NotImplementedError from None
        foreground = None if self.foreground == other.foreground else self.foreground
        background = None if self.background == other.background else self.background
        return Colour(foreground=foreground, background=background)

    def remove_foreground(self) -> Colour:
        return Colour(background=self.background)

    def remove_background(self) -> Colour:
        return Colour(foreground=self.foreground)

    def additive_blend(self, other: ColourType) -> Colour:
        if not isinstance(other, (Colour, RGB, tuple)):
            raise NotImplementedError from None
        foreground = other.foreground if isinstance(other, Colour) else other
        background = other.background if isinstance(other, Colour) else None
        return Colour(
            foreground=self.foreground.additive_blend(foreground),
            background=self.background.additive_blend(background) if background else self.background
        )

    def mean_blend(self, other: ColourType) -> Colour:
        if not isinstance(other, (Colour, RGB, tuple)):
            raise NotImplementedError from None
        foreground = other.foreground if isinstance(other, Colour) else other
        background = other.background if isinstance(other, Colour) else None
        return Colour(
            foreground=self.foreground.mean_blend(foreground),
            background=self.background.mean_blend(background) if background else self.background
        )

    def linear_blend(self, other: ColourType, foreground_bias: float = 0.5, background_bias: float = 0.5) -> Colour:
        if not isinstance(other, (Colour, RGB, tuple)):
            raise NotImplementedError from None
        foreground = other.foreground if isinstance(other, Colour) else other
        background = other.background if isinstance(other, Colour) else None
        return Colour(
            foreground=self.foreground.linear_blend(foreground, bias=foreground_bias),
            background=self.background.linear_blend(background, bias=background_bias) if background else self.background
        )

    def blend(self, other: ColourType, foreground_bias: float = 0.5, background_bias: float = 0.5,
              foreground_gamma: float = 2.2, background_gamma: float = 2.2) -> Colour:
        if not isinstance(other, (Colour, RGB, tuple)):
            raise NotImplementedError from None
        foreground = other.foreground if isinstance(other, Colour) else other
        if isinstance(other, Colour):
            new_background = self.background.blend(other.background, bias=background_bias, gamma=background_gamma)
        else:
            new_background = self.background
        return Colour(
            foreground=self.foreground.blend(foreground, bias=foreground_bias, gamma=foreground_gamma),
            background=new_background
        )

    def __contains__(self, other: ColourType) -> bool:
        if not isinstance(other, (Colour, RGB, tuple)):
            return False
        elif isinstance(other, Colour):
            return self.foreground == other.foreground or self.background == other.background
        elif isinstance(other, RGB):
            return other in (self.foreground, self.background)
        return RGB(*other) in (self.foreground, self.background)

    @cached_property
    def escape_sequence_segment(self) -> str:
        foreground = ";".join(map(str, self.foreground))
        background = ";".join(map(str, self.background))
        return f"38;2;{foreground};48;2;{background}"

    @cached_property
    def has_foreground(self) -> bool:
        return self.foreground != RGBs.DEFAULT_FOREGROUND.value

    @cached_property
    def has_background(self) -> bool:
        return self.background != self.DEFAULT_BACKGROUND

    def __bool__(self) -> bool:
        return self.has_foreground or self.has_background


type ColourType = Colour | RGB | tuple[int, int, int]
