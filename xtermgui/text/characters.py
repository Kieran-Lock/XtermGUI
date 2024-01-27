from enum import StrEnum

from .escape_sequences import AnsiEscapeSequences


class Characters(StrEnum):
    ESCAPE = '\033'
    ZERO_WIDTH = '​'
    BACKSPACE = '\b'
    NEWLINE = '\n'
    TAB = '\t'
    CARRIAGE_RETURN = '\r'
    FORM_FEED = '\f'
    VERTICAL_TAB = '\v'
    TRANSPARENT = str(AnsiEscapeSequences.CURSOR_RIGHT.value())
