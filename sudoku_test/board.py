from __future__ import annotations
from typing import Optional, TYPE_CHECKING
from consolegui import Coordinate, Cursor
if TYPE_CHECKING:
    from .sudoku import Game


class Board:
    EMPTY = " "

    def __init__(self, game: Game) -> None:
        self.game = game
        self._board = [[0 for _ in range(9)] for _ in range(9)]
        self.selected = (0, 0)

    def __getitem__(self, position: Coordinate) -> Optional[int]:
        return self._board[position.y][position.x]

    def __setitem__(self, position: Coordinate, occupant: Optional[int]) -> None:
        self._board[position.y][position.x] = occupant
        Cursor.go_to(Coordinate(position.x * 4 + 2, position.y * 2 + 1))
        if occupant == 0:
            self.game.gui.erase()
        else:
            self.game.gui.print(occupant)

    def __delitem__(self, position: Coordinate) -> None:
        self[position] = 0

    @staticmethod
    def get_empty_board() -> str:
        expand = lambda frame, glue: (glue * 3).join(frame)
        repeat_inner = lambda start, end, minor_boundary, major_boundary: start + (
                    minor_boundary * 2 + major_boundary) * 2 + minor_boundary * 2 + end
        repeat_outer = lambda start, end, minor_boundary, major_boundary, glue: start + (
                    (glue + minor_boundary) * 2 + glue + major_boundary) * 2 + (glue + minor_boundary) * 2 + glue + end
        top = expand(repeat_inner("╔", "╗", "╤", "╦"), "═") + "\n"
        slot_line = expand(repeat_inner("║", "║", "│", "║"), " ") + "\n"
        slot_sep_line = expand(repeat_inner("╟", "╢", "┼", "╫"), "─") + "\n"
        box_sep_line = expand(repeat_inner("╠", "╣", "╪", "╬"), "═") + "\n"
        bottom = expand(repeat_inner("╚", "╝", "╧", "╩"), "═") + "\n"
        return repeat_outer(top, bottom, slot_sep_line, box_sep_line, slot_line)

    def select_slot(self, x: int, y: int) -> None:
        self.selected = (x, y)

    def input_number(self, number: int):
        self[Coordinate(*self.selected)] = number

    def increase_number(self):
        if self[Coordinate(*self.selected)] == 9:
            self[Coordinate(*self.selected)] = 0
        else:
            self[Coordinate(*self.selected)] += 1

    def decrease_number(self):
        if self[Coordinate(*self.selected)] == 0:
            self[Coordinate(*self.selected)] = 9
        else:
            self[Coordinate(*self.selected)] -= 1
