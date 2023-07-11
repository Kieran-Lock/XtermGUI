from .board import Board
from .gui import SudokuGUI


class Game:
    def __init__(self) -> None:
        self.board = Board(self)
        self.gui = SudokuGUI(self.board)
        self.is_playing = False

    def play(self) -> None:
        self.is_playing = True
        with self.gui.start() as gui:
            gui.print(self.board.get_empty_board(), force=True)
            self.board.animate_result(None)
            while self.is_playing:
                pass

    def submit(self) -> None:
        self.board.animate_result(self.board.check_submission())
        self.is_playing = False
