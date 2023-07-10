from sys import stdin
from string import ascii_letters
from typing import Callable
from .keyboard_event import KeyboardEvent
from .mouse_event import MouseEvent
from .keyboard_codes import KeyboardCodes
from .mouse_codes import MouseCodes
from ..geometry import Coordinate


KEYBOARD_CODE_LOOKUP = {
    code.value: code.name for code in KeyboardCodes
}
MOUSE_CODE_LOOKUP = {
    code.value: code.name for code in MouseCodes
}


def read_console() -> KeyboardEvent | MouseEvent | None:
    try:
        read_key = stdin.read(1)
    except TypeError:  # Process terminated
        return
    return determine_event(read_key)


def determine_event(read_key: str) -> KeyboardEvent | MouseEvent:
    key_code = ord(read_key)
    if key_code in range(32, 127):
        return KeyboardEvent(read_key)
    elif key_code == 27:
        return determine_csi_event()
    elif key_code in (8, 9, 10, 127, 163):
        return KeyboardEvent(KEYBOARD_CODE_LOOKUP.get(key_code))
    return KeyboardEvent(KeyboardEvent.UNRECOGNIZED)


def determine_csi_event() -> KeyboardEvent | MouseEvent:
    escape_code = parse_escape_code(lambda character: character and character in ascii_letters + "<~")
    if escape_code in ("[A", "[B", "[C", "[D", "[F", "[H", "[Z"):
        return KeyboardEvent(KEYBOARD_CODE_LOOKUP.get(escape_code))
    elif function_key := get_csi_function_key(escape_code):
        return KeyboardEvent(function_key)
    elif escape_code == "[<":
        return determine_mouse_event()
    elif escape_code[-1] in "~ABCDFH":
        return determine_special_event(escape_code)
    return KeyboardEvent(KeyboardEvent.UNRECOGNIZED)


def parse_escape_code(termination_condition: Callable[[str], bool]) -> str:
    escape_code = ""
    character = ''
    while not termination_condition(character):
        character = stdin.read(1)
        escape_code += character
    return escape_code


def get_csi_function_key(escape_code: str) -> str | None:
    return f"F{ord(stdin.read(1)) - 79}" if escape_code == 'O' else None


def determine_mouse_event() -> MouseEvent:
    mouse_id = parse_escape_code(lambda character: character == ';')[:-1]
    x = int(parse_escape_code(lambda character: character == ';')[:-1]) - 1
    y, last_character = (result := parse_escape_code(lambda character: character and character in "Mm"))[:-1], result[-1]
    if mouse_id in ('0', '1', '2'):
        mouse_id += str(int(last_character == 'M'))

    event = MOUSE_CODE_LOOKUP.get(mouse_id) if mouse_id in (
        "00", "01", "10", "11", "20", "21", "32", "33", "34", "35", "64", "65") else MouseEvent.UNRECOGNIZED
    return MouseEvent(event, Coordinate(x, int(y) - 1))


def determine_special_event(escape_code: str) -> KeyboardEvent:
    escape_code, escape_code_type = escape_code[1:-1], escape_code[-1]
    if escape_code_type == '~' and (code := escape_code.split(';')[0]) in ('2', '3', '5', '6', "15", "17", "18", "19", "20", "21", "23", "24"):
        return KeyboardEvent(KEYBOARD_CODE_LOOKUP.get(code))
    elif escape_code_type in ('A', 'B', 'C', 'D', 'F', 'H'):
        return KeyboardEvent(KEYBOARD_CODE_LOOKUP.get(escape_code_type))
    return KeyboardEvent(KeyboardEvent.UNRECOGNIZED)
