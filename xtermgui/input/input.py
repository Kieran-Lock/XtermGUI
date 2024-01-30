from string import ascii_letters
from sys import stdin
from typing import Callable

from .event import KeyboardEvent, MouseEvent, InputEvent
from .input_codes import KeyboardCode, MouseCode
from ..geometry import Coordinate


def determine_event(read_key: str) -> InputEvent:
    key_code = ord(read_key)
    if key_code in range(32, 127):
        return KeyboardEvent(event=read_key)
    elif key_code == 27:
        return determine_csi_event()
    elif key_code in (8, 9, 10, 127, 163):
        return KeyboardEvent(event=KeyboardCode(str(key_code)))
    return KeyboardEvent.unrecognized()


def determine_csi_event() -> InputEvent:
    escape_code = parse_escape_code(lambda character: character and character in ascii_letters + "<~")
    if escape_code in ("[A", "[B", "[C", "[D", "[F", "[H", "[Z"):
        return KeyboardEvent(event=KeyboardCode(escape_code))
    elif function_key := get_csi_function_key(escape_code):
        return KeyboardEvent(event=function_key)
    elif escape_code == "[<":
        return determine_mouse_event()
    elif escape_code[-1] in "~ABCDFH":
        return determine_special_event(escape_code)
    return KeyboardEvent.unrecognized()


def parse_escape_code(termination_condition: Callable[[str], bool]) -> str:
    escape_code = ""
    character = ''
    while not termination_condition(character):
        character = read_characters(1)
        escape_code += character
    return escape_code


def get_csi_function_key(escape_code: str) -> KeyboardCode | None:
    return KeyboardEvent(event=KeyboardCode(str(ord(read_characters(1))))) if escape_code == 'O' else None


def determine_mouse_event() -> MouseEvent:
    mouse_id = parse_escape_code(lambda character: character == ';')[:-1]
    x = int(parse_escape_code(lambda character: character == ';', )[:-1]) - 1
    y, last_character = (result := parse_escape_code(lambda character: character and character in "Mm"))[:-1], result[
        -1]
    if mouse_id in ('0', '1', '2'):
        mouse_id += str(int(last_character == 'M'))

    coordinate = Coordinate(x, int(y) - 1)
    try:
        return MouseEvent(event=MouseCode(mouse_id), coordinate=coordinate)
    except ValueError:
        return MouseEvent.unrecognized(coordinate=coordinate)


def determine_special_event(escape_code: str) -> KeyboardEvent:
    escape_code, escape_code_type = escape_code[1:-1], escape_code[-1]
    if escape_code_type == '~' and (code := escape_code.split(';')[0]) in (
            '2', '3', '5', '6', "15", "17", "18", "19", "20", "21", "23", "24"):
        return KeyboardEvent(event=KeyboardCode(code))
    elif escape_code_type in ('A', 'B', 'C', 'D', 'F', 'H'):
        return KeyboardEvent(event=KeyboardCode(escape_code_type))
    return KeyboardEvent.unrecognized()


def read_characters(n: int = 1) -> str:
    return stdin.read(n)


def read_event() -> InputEvent | None:
    try:
        read_key = read_characters(1)
    except TypeError:  # Process terminated
        return
    except KeyboardInterrupt:
        raise KeyboardInterrupt("Exited with KeyboardInterrupt.") from None
    return determine_event(read_key)
