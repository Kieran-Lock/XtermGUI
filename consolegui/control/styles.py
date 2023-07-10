from enum import Enum
from .style import Style


class Styles(Enum):
    NOT_STYLED: Style = Style()
    BOLD: Style = Style(bold=True)
    DIMMED: Style = Style(dimmed=True)
    ITALIC: Style = Style(italic=True)
    UNDERLINED: Style = Style(underlined=True)
    HIDDEN: Style = Style(hidden=True)
    CROSSED_OUT: Style = Style(crossed_out=True)
