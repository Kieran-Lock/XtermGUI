from .style import Style


class Styles:
    NOT_STYLED = Style()
    BOLD = Style(bold=True)
    DIMMED = Style(dimmed=True)
    ITALIC = Style(italic=True)
    UNDERLINED = Style(underlined=True)
    HIDDEN = Style(hidden=True)
    CROSSED_OUT = Style(crossed_out=True)
