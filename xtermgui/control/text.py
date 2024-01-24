from __future__ import annotations
from typing import Callable, ClassVar, Iterator
from dataclasses import dataclass
from re import split
from .colour import Colour
from .colours import Colours
from .style import Style
from .styles import Styles
from ..utilities import SupportsLessThan, SupportsString


@dataclass(frozen=True, slots=True)
class Text(str):
    ZERO_WIDTH: ClassVar[str] = '​'
    BACKSPACE: ClassVar[str] = '\b'
    NEWLINE: ClassVar[str] = '\n'
    TAB: ClassVar[str] = '\t'
    CARRIAGE_RETURN: ClassVar[str] = '\r'
    FORM_FEED: ClassVar[str] = '\f'

    text: SupportsString = ""
    colour: Colour = Colours.F_DEFAULT.value
    style: Style = Styles.NOT_STYLED.value

    def __post_init__(self) -> None:
        object.__setattr__(self, "text", str(self.text))

    def __new__(cls, text: SupportsString = "", colour: Colour = Colours.F_DEFAULT.value, style: Style = Styles.NOT_STYLED.value):
        return super(Text, cls).__new__(cls, text)

    def __str__(self) -> str:
        if not self.has_effects:
            return self.text
        return f"{self.escape_code}{self.text}\033[0m"

    @property
    def escape_code(self) -> str:
        escape_code_segments = ";".join(effect.escape_code_segment for effect in (self.colour, self.style) if effect)
        return f"\033[{escape_code_segments}m" if escape_code_segments else ""

    @property
    def has_effects(self) -> bool:
        return bool(self.colour) or bool(self.style)

    def title(self) -> Text:
        non_capitalized = (
            "a", "an", "and", "as", "at", "but", "by", "for", "from",
            "if", "in", "into", "like", "near", "nor", "of", "off",
            "on", "once", "onto", "or", "over", "past", "so", "than",
            "that", "the", "to", "up", "upon", "with", "when", "yet"
        )
        words = split(r"(\S+)", self.text)
        words = words if words[0] else words[1:]
        words = words if words[-1] else words[:-1]
        passed_first = False
        text = "".join(word.capitalize() if ((not word.isspace()) and not passed_first and (passed_first := True) or
                                             (word not in non_capitalized)) else word for word in words)
        return Text(text=text, colour=self.colour, style=self.style)

    def reversed(self) -> Text:
        return Text(text="".join(reversed(self.text)), colour=self.colour, style=self.style)

    def sorted(self, descending: bool = False, key: Callable[[str], SupportsLessThan] | None = None) -> Text:
        return Text(text="".join(sorted(self.text, reverse=descending, key=key)), colour=self.colour, style=self.style)

    def remove_colour(self, colour: Colour) -> Text:
        return Text(self.text, colour=self.colour - colour, style=self.style)

    def set_colour(self, colour: Colour) -> Text:
        return Text(self.text, colour=colour, style=self.style)

    def add_colour(self, colour: Colour) -> Text:
        return Text(self.text, colour=self.colour + colour, style=self.style)

    def remove_style(self, style: Style) -> Text:
        return Text(self.text, colour=self.colour, style=self.style - style)

    def set_style(self, style: Style) -> Text:
        return Text(self.text, colour=self.colour, style=style)

    def add_style(self, style: Style) -> Text:
        return Text(self.text, colour=self.colour, style=self.style + style)

    def __add__(self, other: Text | str) -> Text:
        if isinstance(other, Text):
            text = self.text + other.text
            colour = self.colour + other.colour
            style = self.style + other.style
        else:
            text = self.text + other
            colour = self.colour
            style = self.style
        return Text(text=text, colour=colour, style=style)

    def __contains__(self, item: Style | Colour | Text | str) -> bool:
        if isinstance(item, Style):
            return item in self.style
        elif isinstance(item, Colour):
            return item in self.colour
        elif isinstance(item, Text):
            return item.text in self.text and item.colour in self.colour and item.style in self.style
        elif isinstance(item, str):
            return item in self.text
        return False

    def __iter__(self) -> Iterator[Text]:
        for character in self.text:
            yield Text(text=character, colour=self.colour, style=self.style)

    def __mul__(self, n: int) -> Text:
        return Text(self.text * n, colour=self.colour, style=self.style)

    def __getitem__(self, value: int | slice) -> Text:
        return Text(self.text.__getitem__(value), colour=self.colour, style=self.style)
