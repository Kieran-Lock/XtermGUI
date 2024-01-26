from __future__ import annotations

from dataclasses import dataclass
from functools import cached_property
from typing import ClassVar


@dataclass(frozen=True)
class Style:
    ASCII_STYLE_LOOKUP: ClassVar[dict[str, str]] = {
        "1": "BOLD",
        "2": "DIMMED",
        "3": "ITALIC",
        "4": "UNDERLINED",
        "8": "HIDDEN",
        "9": "CROSSED_OUT",
        "0": "NOT_STYLED"
    }
    bold: bool = False
    dimmed: bool = False
    italic: bool = False
    underlined: bool = False
    hidden: bool = False
    crossed_out: bool = False

    @cached_property
    def styled(self) -> bool:
        return self.bold or self.dimmed or self.italic or self.underlined or self.hidden or self.crossed_out

    @cached_property
    def escape_sequence_segment(self) -> str:
        if not self.styled:
            return "0"
        styles = (self.bold, self.dimmed, self.italic, self.underlined, self.hidden, self.crossed_out)
        return ";".join(style for has_style, style in zip(styles, self.__class__.ASCII_STYLE_LOOKUP) if has_style)

    def __add__(self, other: Style) -> Style:
        return Style(
            self.bold or other.bold,
            self.dimmed or other.dimmed,
            self.italic or other.italic,
            self.underlined or other.underlined,
            self.hidden or other.hidden,
            self.crossed_out or other.crossed_out
        )

    def __sub__(self, other: Style) -> Style:
        return Style(
            self.bold and not other.bold,
            self.dimmed and not other.dimmed,
            self.italic and not other.italic,
            self.underlined and not other.underlined,
            self.hidden and not other.hidden,
            self.crossed_out and not other.crossed_out
        )

    def __contains__(self, style: Style) -> bool:
        return (
                (self.bold and not style.bold) and
                (self.dimmed and not style.dimmed) and
                (self.italic and not style.italic) and
                (self.underlined and not style.underlined) and
                (self.hidden and not style.hidden) and
                (self.crossed_out and not style.crossed_out)
        )

    def __bool__(self) -> bool:
        return self.styled
