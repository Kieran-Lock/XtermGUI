from __future__ import annotations

from dataclasses import dataclass

from .effect import Effect


@dataclass(frozen=True, slots=True, kw_only=True)
class Style(Effect):
    ASCII_STYLE_LOOKUP = {
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

    @property
    def is_styled(self) -> bool:
        return any(self._components)

    @property
    def escape_sequence_segment(self) -> str:
        if not self.is_styled:
            return "0"
        return ";".join(style for has_style, style in zip(self._components, self.ASCII_STYLE_LOOKUP) if has_style)

    @property
    def _components(self) -> tuple[bool, bool, bool, bool, bool, bool]:
        return self.bold, self.dimmed, self.italic, self.underlined, self.hidden, self.crossed_out

    def __add__(self, other: Style) -> Style:
        return Style(
            bold=self.bold or other.bold,
            dimmed=self.dimmed or other.dimmed,
            italic=self.italic or other.italic,
            underlined=self.underlined or other.underlined,
            hidden=self.hidden or other.hidden,
            crossed_out=self.crossed_out or other.crossed_out,
        )

    def __sub__(self, other: Style) -> Style:
        return Style(
            bold=self.bold and not other.bold,
            dimmed=self.dimmed and not other.dimmed,
            italic=self.italic and not other.italic,
            underlined=self.underlined and not other.underlined,
            hidden=self.hidden and not other.hidden,
            crossed_out=self.crossed_out and not other.crossed_out,
        )

    def __contains__(self, style: Style) -> bool:
        return all(component and not other_component for component, other_component in
                   zip(self._components, style._components))
