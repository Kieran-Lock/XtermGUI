from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Iterator

from .characters import Characters
from .colour import Colour
from .colours import Colours
from .escape_sequence import AnsiEscapeSequence
from .escape_sequences import AnsiEscapeSequences
from .style import Style
from .styles import Styles
from ..utilities import SupportsLessThan, SupportsString


@dataclass(frozen=True, slots=True, init=False)
class Text(str):
    text: str
    colour: Colour
    style: Style

    def __init__(self, text: SupportsString, colour: Colour = Colours.F_DEFAULT.value,
                 style: Style = Styles.NOT_STYLED.value) -> None:
        object.__setattr__(self, "text", str(text))
        object.__setattr__(self, "colour", colour)
        object.__setattr__(self, "style", style)

    def __new__(cls, text: SupportsString = "", colour: Colour = Colours.F_DEFAULT.value,
                style: Style = Styles.NOT_STYLED.value):
        return super(Text, cls).__new__(cls, text)

    def __str__(self) -> str:
        if not self.has_effects:
            return self.text
        return f"{self.escape_sequence or ''}{self.text}{AnsiEscapeSequences.END.value}"

    @property
    def escape_sequence(self) -> AnsiEscapeSequence | None:
        escape_sequence_segments = ";".join(
            effect.escape_sequence_segment for effect in (self.colour, self.style) if effect)
        return AnsiEscapeSequence(f"\033[{escape_sequence_segments}m") if escape_sequence_segments else None

    @property
    def has_effects(self) -> bool:
        return bool(self.colour) or bool(self.style)

    def title(self) -> Text:
        non_capitalized = (
            "a", "an", "and", "as", "at", "but", "by", "for", "from",
            "if", "in", "into", "like", "near", "nor", "of", "off",
            "on", "once", "onto", "or", "over", "past", "so", "than",
            "that", "the", "to", "up", "upon", "with", "when", "yet",
        )
        passed_first = False
        text = "".join(word.capitalize() if ((not word.isspace()) and not passed_first and (passed_first := True) or
                                             (word not in non_capitalized)) else word for word in self.text.split())
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

    def __iter__(self) -> Iterator[Text | AnsiEscapeSequence]:
        escape_sequence_matches = AnsiEscapeSequence.matches(self.text)
        offset = 0
        n = len(self.text)
        for i in range(n):
            index = i + offset
            if index >= n:
                return
            character = self.text[index]
            if character == Characters.ESCAPE:
                match = escape_sequence_matches.pop(0)
                yield match.escape_sequence
                offset += match.end - match.start - 1
                continue
            yield Text(text=character, colour=self.colour, style=self.style)

    def __mul__(self, n: int) -> Text:
        return Text(self.text * n, colour=self.colour, style=self.style)

    def __getitem__(self, value: int | slice) -> Text:
        return Text(self.text.__getitem__(value), colour=self.colour, style=self.style)

    @classmethod
    def as_text(cls, value: SupportsString) -> Text:
        return value if isinstance(value, Text) else Text(value)

    @classmethod
    def as_printed(cls, *strings: SupportsString, sep: str = " ", end: str = "\n", flush: bool = False,
                   do_print: bool = False):
        string = str(sep).join(map(str, strings)) + str(end)
        if do_print:
            print(string, end="", flush=flush)
        return cls.as_text(string)

    def replace_at(self, start_index: int, replacement: str, n: int = 1, ) -> Text:
        return Text(self.text[:start_index] + replacement + self.text[start_index + n:], colour=self.colour,
                    style=self.style)
