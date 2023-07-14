from enum import Enum
from .colour import Colour
from .rgbs import RGBs


class Colours(Enum):
    F_BLACK: Colour = Colour(foreground=RGBs.BLACK.value)
    F_WHITE: Colour = Colour(foreground=RGBs.WHITE.value)
    F_RED: Colour = Colour(foreground=RGBs.RED.value)
    F_GREEN: Colour = Colour(foreground=RGBs.GREEN.value)
    F_BLUE: Colour = Colour(foreground=RGBs.BLUE.value)
    F_YELLOW: Colour = Colour(foreground=RGBs.YELLOW.value)
    F_CYAN: Colour = Colour(foreground=RGBs.CYAN.value)
    F_MAGENTA: Colour = Colour(foreground=RGBs.MAGENTA.value)
    F_ORANGE: Colour = Colour(foreground=RGBs.ORANGE.value)
    F_PURPLE: Colour = Colour(foreground=RGBs.PURPLE.value)
    F_GREY: Colour = Colour(foreground=RGBs.GREY.value)
    F_BROWN: Colour = Colour(foreground=RGBs.BROWN.value)
    F_DEFAULT: Colour = Colour(foreground=RGBs.DEFAULT_FOREGROUND.value)

    B_BLACK: Colour = Colour(background=RGBs.BLACK.value)
    B_WHITE: Colour = Colour(background=RGBs.WHITE.value)
    B_RED: Colour = Colour(background=RGBs.RED.value)
    B_GREEN: Colour = Colour(background=RGBs.GREEN.value)
    B_BLUE: Colour = Colour(background=RGBs.BLUE.value)
    B_YELLOW: Colour = Colour(background=RGBs.YELLOW.value)
    B_CYAN: Colour = Colour(background=RGBs.CYAN.value)
    B_MAGENTA: Colour = Colour(background=RGBs.MAGENTA.value)
    B_ORANGE: Colour = Colour(background=RGBs.ORANGE.value)
    B_PURPLE: Colour = Colour(background=RGBs.PURPLE.value)
    B_GREY: Colour = Colour(background=RGBs.GREY.value)
    B_BROWN: Colour = Colour(background=RGBs.BROWN.value)
    B_DEFAULT_PYCHARM: Colour = Colour(background=RGBs.DEFAULT_BACKGROUND_PYCHARM.value)
    B_DEFAULT_REPLIT: Colour = Colour(background=RGBs.DEFAULT_BACKGROUND_REPLIT.value)
    B_DEFAULT_BACKGROUND_WSL = Colour(background=RGBs.DEFAULT_BACKGROUND_WSL.value)
