from enum import StrEnum


class KeyboardCode(StrEnum):
    SHIFT_BACKSPACE = "8"
    TAB = "9"
    ENTER = "10"
    BACKSPACE = "127"
    POUND = "163"
    UP_ARROW = "[A"
    DOWN_ARROW = "[B"
    RIGHT_ARROW = "[C"
    LEFT_ARROW = "[D"
    END = "[F"
    HOME = "[H"
    SHIFT_TAB = "[Z"
    INSERT = "2"
    DELETE = "3"
    PAGE_UP = "5"
    PAGE_DOWN = "6"
    F1 = "80"
    F2 = "81"
    F3 = "82"
    F4 = "83"
    F5 = "15"
    F6 = "17"
    F7 = "18"
    F8 = "19"
    F9 = "20"
    F10 = "21"
    F11 = "23"
    F12 = "24"


class MouseCode(StrEnum):
    LEFT_MOUSE_UP = "00"
    LEFT_MOUSE_DOWN = "01"
    MIDDLE_MOUSE_UP = "10"
    MIDDLE_MOUSE_DOWN = "11"
    RIGHT_MOUSE_UP = "20"
    RIGHT_MOUSE_DOWN = "21"
    LEFT_MOUSE_DRAG = "32"
    MIDDLE_MOUSE_DRAG = "33"
    RIGHT_MOUSE_DRAG = "34"
    MOVE = "35"
    SCROLL_UP = "64"
    SCROLL_DOWN = "65"
