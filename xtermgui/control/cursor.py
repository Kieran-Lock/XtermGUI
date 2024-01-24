from __future__ import annotations

from sys import stdout, stdin

from .text import Text
from ..geometry import Coordinate
from ..input import parse_escape_code
from ..utilities import console_inputs


class Cursor:
    position: Coordinate = Coordinate(0, 0)
    visible: bool = True

    @classmethod
    def get_live_position(cls) -> Coordinate:
        with console_inputs():
            stdout.write("\033[6n")
            stdout.flush()
            stdin.read(2)
            raw_position = parse_escape_code(lambda c: c == "R")[:-1]
        return Coordinate(*map(int, reversed(raw_position.split(";")))) - (1, 1)

    @classmethod
    def up(cls, n: int = 1) -> type[Cursor]:
        if not isinstance(n, int):
            raise NotImplementedError from None
        stdout.write(f"\033[{n}A")
        stdout.flush()
        cls.position -= (0, n)
        return cls

    @classmethod
    def down(cls, n: int = 1) -> type[Cursor]:
        if not isinstance(n, int):
            raise NotImplementedError from None
        stdout.write(f"\033[{n}B")
        stdout.flush()
        cls.position += (0, n)
        return cls

    @classmethod
    def left(cls, n: int = 1) -> type[Cursor]:
        if not isinstance(n, int):
            raise NotImplementedError from None
        stdout.write(f"\033[{n}D")
        stdout.flush()
        cls.position -= (n, 0)
        return cls

    @classmethod
    def right(cls, n: int = 1) -> type[Cursor]:
        if not isinstance(n, int):
            raise NotImplementedError from None
        stdout.write(f"\033[{n}C")
        stdout.flush()
        cls.position += (n, 0)
        return cls

    @classmethod
    def go_to(cls, coordinate: Coordinate | tuple[int, int]) -> type[Cursor]:
        if not isinstance(coordinate, (Coordinate, tuple)):
            raise NotImplementedError from None
        elif isinstance(coordinate, tuple) and tuple(map(type, coordinate)) != (int, int):
            raise NotImplementedError from None
        coordinate = coordinate if isinstance(coordinate, Coordinate) else Coordinate(*coordinate)
        stdout.write(f"\033[{coordinate.y + 1};{coordinate.x + 1}H")
        stdout.flush()
        cls.position = coordinate
        return cls

    @classmethod
    def update_position_on_print(cls, character: str) -> None:
        match character:
            case Text.ZERO_WIDTH:
                pass
            case Text.BACKSPACE:
                cls.position -= (1, 0)
            case Text.NEWLINE:
                cls.position = Coordinate(0, cls.position.y + 1)
            case Text.TAB:
                cls.position += (4, 0)
            case Text.CARRIAGE_RETURN:
                cls.position = Coordinate(0, cls.position.y)
            case Text.FORM_FEED:
                cls.position = Coordinate(cls.position.x + 1, cls.position.y + 1)
            case _:
                cls.position += (1, 0)

    @classmethod
    def show(cls) -> None:
        stdout.write("\033[?25h")
        stdout.flush()
        cls.visible = True

    @classmethod
    def hide(cls) -> None:
        stdout.write("\033[?25l")
        stdout.flush()
        cls.visible = False

    @staticmethod
    def clear_line(before_cursor: bool = True, after_cursor: bool = True) -> None:
        if not (before_cursor or after_cursor):
            return
        elif not before_cursor:
            stdout.write("\033[K")
        elif not after_cursor:
            stdout.write("\033[1K")
        else:
            stdout.write("\033[2K")
        stdout.flush()


Cursor.position = Cursor.get_live_position()
