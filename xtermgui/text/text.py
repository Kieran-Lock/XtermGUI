from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Iterator

from unicodedata import category

from .character_info import CharacterInfo
from .characters import Characters
from .escape_sequence import AnsiEscapeSequence
from .escape_sequences import AnsiEscapeSequences
from .style import Style
from .styles import Styles
from .text_colour import TextColour
from .text_colours import ForegroundColours
from ..utilities import SupportsLessThan, SupportsString


@dataclass(frozen=True, slots=True, init=False)
class Text(str):
    text: str
    colour: TextColour
    style: Style

    def __init__(self, text: SupportsString, colour: TextColour = ForegroundColours.DEFAULT,
                 style: Style = Styles.NOT_STYLED) -> None:
        object.__setattr__(self, "text", str(text))
        object.__setattr__(self, "colour", colour)
        object.__setattr__(self, "style", style)

    def __new__(cls, text: SupportsString = "", colour: TextColour = ForegroundColours.DEFAULT,
                style: Style = Styles.NOT_STYLED):
        return super(Text, cls).__new__(cls, text)

    def __str__(self) -> str:
        if not self.has_effects:
            return self.text
        return f"{self.escape_sequence or ''}{self.text}{AnsiEscapeSequences.END}"

    @property
    def escape_sequence(self) -> AnsiEscapeSequence | None:
        escape_sequence_segments = ";".join(
            effect.escape_sequence_segment for effect in (self.colour, self.style) if effect)
        return AnsiEscapeSequence(f"\033[{escape_sequence_segments}m") if escape_sequence_segments else None

    @property
    def has_effects(self) -> bool:
        return self.colour.has_foreground or self.colour.has_background or self.style.is_styled

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

    def remove_colour(self, colour: TextColour) -> Text:
        return Text(self.text, colour=self.colour - colour, style=self.style)

    def set_colour(self, colour: TextColour) -> Text:
        return Text(self.text, colour=colour, style=self.style)

    def add_colour(self, colour: TextColour) -> Text:
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

    def __contains__(self, item: Style | TextColour | Text | str) -> bool:
        if isinstance(item, Style):
            return item in self.style
        elif isinstance(item, TextColour):
            return item in self.colour
        elif isinstance(item, Text):
            return item.text in self.text and item.colour in self.colour and item.style in self.style
        elif isinstance(item, str):
            return item in self.text
        return False

    def __iter__(self) -> Iterator[CharacterInfo]:
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
                yield CharacterInfo(match.escape_sequence, index)
                offset += match.end - match.start - 1
                continue
            yield CharacterInfo(Text(text=character, colour=self.colour, style=self.style), index)

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

    @staticmethod
    def character_is_transparent(character: str) -> bool:
        if len(character) > 1:
            if AnsiEscapeSequence.is_valid(character):
                return True
            raise ValueError("Must pass a single character for transparency checks.") from None
        return isinstance(character, AnsiEscapeSequence) or character in (
            Characters.ESCAPE,
            Characters.ZERO_WIDTH,
            Characters.BACKSPACE,
            Characters.NEWLINE,
            Characters.TAB,
            Characters.CARRIAGE_RETURN,
        ) or category(character)[0] in "MC"
