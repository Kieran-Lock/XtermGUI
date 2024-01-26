from enum import StrEnum

from .escape_sequences import StaticAnsiEscapeSequences


class Characters(StrEnum):
    ESCAPE = '\033'
    ZERO_WIDTH = '​'
    BACKSPACE = '\b'
    NEWLINE = '\n'
    TAB = '\t'
    CARRIAGE_RETURN = '\r'
    FORM_FEED = '\f'
    VERTICAL_TAB = '\v'
    TRANSPARENT = str(StaticAnsiEscapeSequences.CURSOR_FORWARD_ONE.value)
