from __future__ import annotations

from typing import NamedTuple, TYPE_CHECKING

from .escape_sequence import AnsiEscapeSequence

if TYPE_CHECKING:
    from .text import Text


class CharacterInfo(NamedTuple):
    character: Text | AnsiEscapeSequence
    index: int
