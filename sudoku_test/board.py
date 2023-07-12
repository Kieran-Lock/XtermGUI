from __future__ import annotations
from typing import Optional, TYPE_CHECKING, Iterable
from itertools import chain
from consolegui import Coordinate, Cursor, Text, Colours
if TYPE_CHECKING:
    from .sudoku import Game


class Board:
    EMPTY = " "

    def __init__(self, game: Game) -> None:
        self.game = game
        self._board = [[0 for _ in range(9)] for _ in range(9)]
        self._board = [
            [2, 9, 5, 7, 4, 3, 8, 6, 1],
            [4, 3, 1, 8, 6, 5, 9, 2, 7],
            [8, 7, 6, 1, 9, 2, 5, 4, 3],
            [3, 8, 7, 4, 5, 9, 2, 1, 6],
            [6, 1, 2, 3, 8, 7, 4, 9, 5],
            [5, 4, 9, 2, 1, 6, 7, 3, 8],
            [7, 6, 3, 5, 2, 4, 1, 8, 9],
            [9, 2, 8, 6, 7, 1, 3, 5, 4],
            [1, 5, 4, 9, 3, 8, 6, 7, 2]
        ]
        self.selected = Coordinate(0, 0)
        self.write_colour = Colours.F_DEFAULT.value

    def __getitem__(self, position: Coordinate) -> Optional[int]:
        return self._board[position.y][position.x]

    def __setitem__(self, position: Coordinate, occupant: Optional[int]) -> None:
        existing = self[position]
        Cursor.go_to(Coordinate(position.x * 4 + 2, position.y * 2 + 1))
        if not existing:
            pass
        elif occupant == 0:
            self.game.gui.erase()
        else:
            self.game.gui.print(Text(occupant).set_colour(self.write_colour))
        self._board[position.y][position.x] = occupant

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

    def select_slot(self, coordinate: Coordinate) -> None:
        self.selected = coordinate

    def input_number(self, number: int):
        self[self.selected] = number

    def increase_number(self):
        if self[self.selected] == 9:
            self[self.selected] = 0
        else:
            self[self.selected] += 1

    def decrease_number(self):
        if self[self.selected] == 0:
            self[self.selected] = 9
        else:
            self[self.selected] -= 1

    def check_submission(self) -> bool:
        def get_block(board: list[list[int]], x: int, y: int) -> chain:
            return chain(*[board[i][3 * x:3 * x + 3] for i in range(3 * y, 3 * y + 3)])

        def correct_entries(entries: Iterable) -> bool:
            result = 0
            for entry in entries:
                if not entry:
                    continue
                result |= 1 << (entry - 1)
            return result == 511

        rows_correct = all(map(correct_entries, self._board))
        if not rows_correct:
            return False
        columns_correct = all(map(correct_entries, zip(*self._board)))
        if not columns_correct:
            return False
        return all(map(correct_entries, (get_block(self._board, x, y) for x in range(0, 3) for y in range(0, 3))))

    def animate_result(self, success: bool | None) -> None:
        def get_anti_diagonal_coordinates(board: list[list[int]]) -> Iterable[Coordinate]:
            height, width = len(board), len(board[0])
            return (Coordinate(q, p - q) for p in range(height + width - 1) for q in
                    range(max(p - height + 1, 0), min(p + 1, width)))

        self.write_colour = Colours.F_GREEN.value if success else Colours.F_DEFAULT.value if success is None else Colours.F_RED.value
        for coordinate in get_anti_diagonal_coordinates(self._board):
            self[coordinate] = self[coordinate]
        if success is None:
            return
        feedback_string = "You solved the sudoku!" if success else "You failed to solve the sudoku!"
        self.game.gui.print(Text(feedback_string).set_colour(self.write_colour), at=Coordinate(0, 20))
