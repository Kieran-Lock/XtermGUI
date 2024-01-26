from enum import StrEnum

from .escape_sequences import DynamicAnsiEscapeSequences


class Characters(StrEnum):
    ESCAPE = '\033'
    ZERO_WIDTH = '​'
    BACKSPACE = '\b'
    NEWLINE = '\n'
    TAB = '\t'
    CARRIAGE_RETURN = '\r'
    FORM_FEED = '\f'
    VERTICAL_TAB = '\v'
    TRANSPARENT = str(DynamicAnsiEscapeSequences.CURSOR_RIGHT.value())
