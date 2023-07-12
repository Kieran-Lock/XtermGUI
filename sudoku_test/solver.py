from __future__ import annotations
from typing import TYPE_CHECKING, Iterable, Callable, Any
import itertools
from consolegui import Coordinate
from .entry import Entry


if TYPE_CHECKING:
    from sudoku_test.board import Board


def intersect(a, b):
    return a & b


def value_to_bits(value):
    return 1 << (value - 1)


class SudokuSolver:
    def __init__(self, board: Board) -> None:
        self.board = board
        self.row_pool = [self.row_to_bits(row) for row in range(9)]
        self.column_pool = [self.column_to_bits(column) for column in range(9)]
        self.box_pool = [self.box_to_bits(box) for box in range(9)]

    def row_to_bits(self, row: int) -> int:
        total = 0
        for item in self.board[row]:
            if not item:
                continue
            total += value_to_bits(item)
        return 0b111111111 ^ total

    def column_to_bits(self, column: int) -> int:
        total = 0
        for row in self.board:
            item = row[column]
            if not item:
                continue
            total += value_to_bits(item)
        return 0b111111111 ^ total

    def box_to_bits(self, box: int) -> int:
        total = 0
        y, x = (*map(3 .__mul__, divmod(box, 3)),)
        for y, x in itertools.product(range(y, y + 3), range(x, x + 3)):
            item = self.board[y][x]
            if not item:
                continue
            total += value_to_bits(item)
        return 0b111111111 ^ total

    def make_guess(self, coordinate: Coordinate, guess: Entry) -> None:
        self.board[coordinate] = guess
        self.row_pool[coordinate.y] &= ~value_to_bits(self.board[coordinate])
        self.column_pool[coordinate.x] &= ~value_to_bits(self.board[coordinate])
        self.box_pool[self.box(coordinate)] &= ~value_to_bits(self.board[coordinate])

    def erase_guess(self, coordinate: Coordinate) -> None:
        self.row_pool[coordinate.y] += value_to_bits(self.board[coordinate])
        self.column_pool[coordinate.x] += value_to_bits(self.board[coordinate])
        self.box_pool[self.box(coordinate)] += value_to_bits(self.board[coordinate])
        self.board[coordinate] = Entry(0)

    def solve(self, interval_callback: Callable[[Any, ...], Any] | None = None, *args: Any, **kwargs: Any) -> bool:
        coordinate = self.next()
        if coordinate is None:
            return True
        for guess in self.get_valid_guesses(coordinate):
            self.make_guess(coordinate, guess)
            if interval_callback is not None:
                interval_callback(*args, **kwargs)
            if self.solve():
                return True
            self.erase_guess(coordinate)
        return False

    @staticmethod
    def box(coordinate: Coordinate) -> int:
        return coordinate.y // 3 * 3 + coordinate.x // 3

    def get_valid_guesses(self, coordinate: Coordinate) -> Iterable[Entry]:
        valid_guesses = intersect(intersect(self.row_pool[coordinate.y], self.column_pool[coordinate.x]), self.box_pool[self.box(coordinate)])
        return (Entry(i + 1) for i in range(9) if valid_guesses & (1 << i))

    def next(self) -> Coordinate | None:
        for y in range(9):
            for x in range(9):
                coordinate = Coordinate(x, y)
                if self.board[coordinate].is_empty():
                    return coordinate
        return None
