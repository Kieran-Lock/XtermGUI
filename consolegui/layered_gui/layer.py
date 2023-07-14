from __future__ import annotations
from typing import Iterator, TYPE_CHECKING
from dataclasses import dataclass, field
from contextlib import contextmanager
from ..control import Cursor, SupportsString
from ..geometry import Coordinate
if TYPE_CHECKING:
    from .gui import LayeredGUI


@dataclass(slots=True, order=True)
class Layer:
    gui: LayeredGUI = field(compare=False, repr=False)
    name: str = field(compare=False)
    z: float
    content: dict[Coordinate, SupportsString] = field(compare=False, init=False, default_factory=dict, repr=False)

    def write(self, text: SupportsString, at: Coordinate | None = None):
        if at is None:
            at = Cursor.position
        self.content[at] = text

    def erase_content(self, at: Coordinate | None = None):
        if at is None:
            at = Cursor.position
        if at in self.content:
            del self.content[at]

    def can_print_at(self, at: Coordinate) -> bool:
        starting_index = self.gui.layers.index(self.gui.get_layer(lambda layer: self is layer)) + 1
        return not any(layer.is_occupied_at(at) for layer in self.gui.traverse_layers(start=starting_index))

    def new_character_on_erase_at(self, at: Coordinate) -> SupportsString | None:
        if not self.can_print_at(at):
            return
        starting_index = len(self.gui.layers) - self.gui.layers.index(self.gui.get_layer(lambda layer: self is layer))
        for layer in self.gui.traverse_layers(start=starting_index, reverse=True):
            if layer.is_occupied_at(at):
                return layer.content[at]
        return self.gui.__class__.ERASE_CHARACTER
    
    def is_occupied_at(self, at: Coordinate) -> bool:
        return at in self.content

    def clear_content(self) -> None:
        self.content = {}

    def get_size(self) -> Coordinate:
        if not self.content:
            return Coordinate(0, 0)
        x = max(self.content, key=lambda coordinate: coordinate.x).x
        y = max(self.content, key=lambda coordinate: coordinate.y).y
        return Coordinate(x, y)
