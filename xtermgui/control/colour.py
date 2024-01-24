from __future__ import annotations
from functools import cached_property
from dataclasses import dataclass, field
from typing import ClassVar, Optional
from .rgb import RGB
from .rgbs import RGBs


@dataclass(frozen=True)
class _Colour:
    DEFAULT_BACKGROUND: ClassVar[RGB] = RGBs.DEFAULT_BACKGROUND_WSL.value

    _foreground: Optional[RGB | tuple[int, int, int]] = None
    _background: Optional[RGB | tuple[int, int, int]] = None
    _initialized: bool = field(default=False, init=False, repr=False)

    @property
    def foreground(self) -> RGB | tuple[int, int, int]:
        return self._foreground if self._foreground is not None else RGBs.DEFAULT_FOREGROUND.value

    @foreground.setter
    def foreground(self, value: RGB | tuple[int, int, int]) -> None:
        if self._initialized:
            raise NotImplementedError from None
        object.__setattr__(self, "_foreground", value)

    @property
    def background(self):
        return self._background if self._background is not None else self.__class__.DEFAULT_BACKGROUND

    @background.setter
    def background(self, value: RGB | tuple[int, int, int]) -> None:
        if self._initialized:
            raise NotImplementedError from None
        object.__setattr__(self, "_background", value)
    
    @classmethod
    def configure_default_background(cls, rgb: RGB) -> RGB:
        cls.DEFAULT_BACKGROUND = rgb
        return cls.DEFAULT_BACKGROUND

    def __post_init__(self) -> None:
        if not isinstance(self.foreground, (Colour, RGB, tuple)) and self.foreground is not None:
            raise ValueError(f"Cannot initialize colour with {self.foreground = }") from None
        elif not isinstance(self.background, (Colour, RGB, tuple)) and self.background is not None:
            raise ValueError(f"Cannot initialize colour with {self.background = }") from None
        foreground = RGBs.DEFAULT_FOREGROUND.value if self.foreground is None else self.foreground
        background = self.__class__.DEFAULT_BACKGROUND if self.background is None else self.background
        foreground = foreground if isinstance(foreground, RGB) else RGB(*foreground)
        background = background if isinstance(background, RGB) else RGB(*background)
        object.__setattr__(self, "foreground", foreground)
        object.__setattr__(self, "background", background)
        object.__setattr__(self, "_initialized", True)

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
    def escape_code_segment(self) -> str:
        foreground = ";".join(map(str, self.foreground))
        background = ";".join(map(str, self.background))
        return f"38;2;{foreground};48;2;{background}"

    @cached_property
    def has_foreground(self) -> bool:
        return self.foreground != RGBs.DEFAULT_FOREGROUND.value

    @cached_property
    def has_background(self) -> bool:
        return self.background != self.__class__.DEFAULT_BACKGROUND

    def __bool__(self) -> bool:
        return self.has_foreground or self.has_background


class Colour(_Colour):
    def __init__(self, foreground: Optional[RGB | tuple[int, int, int]] = None, background: Optional[RGB | tuple[int, int, int]] = None) -> None:
        super().__init__(foreground, background)

    def __repr__(self):
        return super().__repr__().replace("_", "")


ColourType = Colour | RGB | tuple[int, int, int]
