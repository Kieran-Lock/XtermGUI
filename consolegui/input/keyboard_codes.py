from enum import Enum


class KeyboardCodes(Enum):
    SHIFT_BACKSPACE: int = 8
    TAB: int = 9
    ENTER: int = 10
    BACKSPACE: int = 127
    POUND: int = 163

    UP_ARROW: str = "[A"
    DOWN_ARROW: str = "[B"
    RIGHT_ARROW: str = "[C"
    LEFT_ARROW: str = "[D"
    END: str = "[F"
    HOME: str = "[H"
    SHIFT_TAB: str = "[Z"

    INSERT: str = "2"
    DELETE: str = "3"
    PAGE_UP: str = "5"
    PAGE_DOWN: str = "6"
    F5: str = "15"
    F6: str = "17"
    F7: str = "18"
    F8: str = "19"
    F9: str = "20"
    F10: str = "21"
    F11: str = "23"
    F12: str = "24"
