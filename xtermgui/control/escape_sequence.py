from __future__ import annotations

from dataclasses import dataclass
from re import compile, Pattern, finditer
from typing import ClassVar, NamedTuple, Literal

from ..geometry import Coordinate


class Match(NamedTuple):
    start: int
    end: int
    escape_sequence: AnsiEscapeSequence


@dataclass(frozen=True, slots=True, init=False)
class AnsiEscapeSequence(str):
    REGEX: ClassVar[Pattern] = compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")

    escape_sequence: str
    cursor_print_displacement: Coordinate

    def __init__(self, escape_sequence: str, cursor_print_displacement: Coordinate = Coordinate(0, 0),
                 validate: bool = True) -> None:
        if validate and not self.is_valid(escape_sequence):
            raise ValueError("Cannot create invalid ANSI escape sequence.") from None
        object.__setattr__(self, "escape_sequence", escape_sequence)
        object.__setattr__(self, "cursor_print_displacement", cursor_print_displacement)

    def __new__(cls, text: str):
        return super(AnsiEscapeSequence, cls).__new__(cls, text)

    def __str__(self) -> str:
        return self.escape_sequence

    def __len__(self) -> Literal[1]:
        return 1

    @classmethod
    def is_valid(cls, escape_sequence: str) -> bool:
        return cls.REGEX.match(escape_sequence) is not None

    @classmethod
    def matches(cls, string: str) -> list[Match]:
        return [Match(*match.span(), cls(match.string, validate=False)) for match in finditer(cls.REGEX, string)]

    def execute(self, flush: bool = True) -> None:
        print(self, end="", flush=flush)
