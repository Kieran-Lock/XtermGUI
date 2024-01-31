from __future__ import annotations

from dataclasses import dataclass
from typing import ClassVar

from .colour import Colour
from .colours import Colours
from .effect import Effect


@dataclass(frozen=True, slots=True, init=False, kw_only=True)
class TextColour(Effect):
    DEFAULT_BACKGROUND: ClassVar[Colour] = Colours.DEFAULT_BACKGROUND_WSL

    foreground: Colour
    background: Colour

    def __init__(self, foreground: Colour | tuple[int, int, int] | None = None,
                 background: Colour | tuple[int, int, int] | None = None) -> None:
        foreground = Colours.DEFAULT_FOREGROUND if foreground is None else foreground
        background = self.DEFAULT_BACKGROUND if background is None else background
        foreground = foreground if isinstance(foreground, Colour) else Colour(*foreground)
        background = background if isinstance(background, Colour) else Colour(*background)
        object.__setattr__(self, "foreground", foreground)
        object.__setattr__(self, "background", background)

    @classmethod
    def configure_default_background(cls, rgb: Colour) -> None:
        cls.DEFAULT_BACKGROUND = rgb

    def __add__(self, other: TextColour) -> TextColour:
        return TextColour(
            foreground=self.foreground if self.has_foreground else other.foreground,
            background=self.background if self.has_background else other.background,
        )

    def __sub__(self, other: TextColour) -> TextColour:
        return TextColour(
            foreground=None if self.foreground == other.foreground else self.foreground,
            background=None if self.background == other.background else self.background,
        )

    def remove_foreground(self) -> TextColour:
        return TextColour(background=self.background)

    def remove_background(self) -> TextColour:
        return TextColour(foreground=self.foreground)

    def new_foreground(self, foreground: Colour) -> TextColour:
        return TextColour(foreground=foreground, background=self.background)

    def new_background(self, background: Colour) -> TextColour:
        return TextColour(foreground=self.foreground, background=background)

    def __contains__(self, other: Colour) -> bool:
        return other in (self.foreground, self.background)

    @property
    def escape_sequence_segment(self) -> str:
        foreground = ";".join(map(str, self.foreground))
        background = ";".join(map(str, self.background))
        return f"38;2;{foreground};48;2;{background}"

    @property
    def has_foreground(self) -> bool:
        return self.foreground != Colours.DEFAULT_FOREGROUND

    @property
    def has_background(self) -> bool:
        return self.background != self.DEFAULT_BACKGROUND

    def __bool__(self) -> bool:
        return self.has_foreground or self.has_background
