from __future__ import annotations

from contextlib import contextmanager
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Iterator, Self

from ..control import Cursor
from ..geometry import Coordinate
from ..utilities import SupportsString

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
        return Coordinate(
            max(coordinate.x for coordinate in self.content),
            max(coordinate.y for coordinate in self.content),
        )

    @contextmanager
    def as_active(self) -> Iterator[Self]:
        previous_active_layer = self.gui.active_layer
        self.gui.active_layer = self
        try:
            yield self
        finally:
            self.gui.active_layer = previous_active_layer
