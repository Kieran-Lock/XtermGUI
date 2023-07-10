from .board import Board
from .gui import SudokuGUI


class Game:
    def __init__(self) -> None:
        self.board = Board(self)
        self.gui = SudokuGUI(self.board)

    def play(self) -> None:
        with self.gui.start() as gui:
            gui.print(self.board.get_empty_board(), force=True)
            while True:
                pass
