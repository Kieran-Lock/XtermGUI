from consolegui import LayeredGUI, Region, MouseEvent, KeyboardEvent, MouseInteraction, KeyboardInteraction, Events, Coordinate


SELECT_SLOT_INTERACTION_REGION = Region(Coordinate(0, 0), Coordinate(36, 0), Coordinate(36, 18), Coordinate(0, 18))


class SudokuGUI(LayeredGUI):
    def __init__(self, board) -> None:
        super().__init__()
        self.board = board

    @MouseInteraction(Events.LEFT_MOUSE_DOWN.value, SELECT_SLOT_INTERACTION_REGION)
    def select_slot(self, event: MouseEvent) -> None:
        self.board.select_slot(Coordinate(event.coordinate.x // 4, event.coordinate.y // 2))

    @KeyboardInteraction(Events.ANY_KEYBOARD.value)
    def input_number(self, event: KeyboardEvent) -> None:
        if event.name in list(map(str, range(10))):
            self.board.input_number(int(event.name))

    @KeyboardInteraction(Events.LEFT_ARROW.value)
    def decrease_number(self, event: KeyboardEvent) -> None:
        self.board.decrease_number()

    @KeyboardInteraction(Events.RIGHT_ARROW.value)
    def increase_number(self, event: KeyboardEvent) -> None:
        self.board.increase_number()

    @KeyboardInteraction(Events.ENTER.value)
    def submit_sudoku(self, event: KeyboardEvent) -> None:
        self.board.game.submit()

    @KeyboardInteraction(Events.SPACE.value)
    def demonstrate_solve(self, event: KeyboardEvent) -> None:
        self.board.solve()
