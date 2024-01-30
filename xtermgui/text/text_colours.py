from .colours import Colours
from .text_colour import TextColour


class ForegroundColours:
    BLACK = TextColour(foreground=Colours.BLACK)
    WHITE = TextColour(foreground=Colours.WHITE)
    RED = TextColour(foreground=Colours.RED)
    GREEN = TextColour(foreground=Colours.GREEN)
    BLUE = TextColour(foreground=Colours.BLUE)
    YELLOW = TextColour(foreground=Colours.YELLOW)
    CYAN = TextColour(foreground=Colours.CYAN)
    MAGENTA = TextColour(foreground=Colours.MAGENTA)
    ORANGE = TextColour(foreground=Colours.ORANGE)
    PURPLE = TextColour(foreground=Colours.PURPLE)
    GREY = TextColour(foreground=Colours.GREY)
    BROWN = TextColour(foreground=Colours.BROWN)
    DEFAULT = TextColour(foreground=Colours.DEFAULT_FOREGROUND)


class BackgroundColours:
    BLACK = TextColour(background=Colours.BLACK)
    WHITE = TextColour(background=Colours.WHITE)
    RED = TextColour(background=Colours.RED)
    GREEN = TextColour(background=Colours.GREEN)
    BLUE = TextColour(background=Colours.BLUE)
    YELLOW = TextColour(background=Colours.YELLOW)
    CYAN = TextColour(background=Colours.CYAN)
    MAGENTA = TextColour(background=Colours.MAGENTA)
    ORANGE = TextColour(background=Colours.ORANGE)
    PURPLE = TextColour(background=Colours.PURPLE)
    GREY = TextColour(background=Colours.GREY)
    BROWN = TextColour(background=Colours.BROWN)
    DEFAULT_PYCHARM = TextColour(background=Colours.DEFAULT_BACKGROUND_PYCHARM)
    DEFAULT_REPLIT = TextColour(background=Colours.DEFAULT_BACKGROUND_REPLIT)
    DEFAULT_BACKGROUND_WSL = TextColour(background=Colours.DEFAULT_BACKGROUND_WSL)
