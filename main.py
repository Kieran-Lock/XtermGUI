from sudoku_test import Game
from consolegui import Colour, RGBs


Colour.configure_default_background(RGBs.DEFAULT_BACKGROUND_WSL.value)
Game().play()
