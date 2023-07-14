from enum import Enum


class MouseCodes(Enum):
    LEFT_MOUSE_UP: str = "00"
    LEFT_MOUSE_DOWN: str = "01"
    MIDDLE_MOUSE_UP: str = "10"
    MIDDLE_MOUSE_DOWN: str = "11"
    RIGHT_MOUSE_UP: str = "20"
    RIGHT_MOUSE_DOWN: str = "21"
    LEFT_MOUSE_DRAG: str = "32"
    MIDDLE_MOUSE_DRAG: str = "33"
    RIGHT_MOUSE_DRAG: str = "34"
    MOVE: str = "35"
    SCROLL_UP: str = "64"
    SCROLL_DOWN: str = "65"
