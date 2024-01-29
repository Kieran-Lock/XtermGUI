from __future__ import annotations

from contextlib import contextmanager
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Iterator, Self

from ..geometry import Coordinate
from ..terminal import terminal
from ..utilities import SupportsString

if TYPE_CHECKING:
    from .gui import LayeredGUI


@dataclass(slots=True)
class Layer:
    gui: LayeredGUI = field(repr=False)
    name: str
    z: float
    content: dict[Coordinate, SupportsString] = field(init=False, default_factory=dict, repr=False)

    def write(self, text: SupportsString, at: Coordinate | None = None):
        if at is None:
            at = terminal.cursor.position
        self.content[at] = text

    def erase_content(self, at: Coordinate | None = None):
        if at is None:
            at = terminal.cursor.position
        if at in self.content:
            del self.content[at]

    def can_print_at(self, at: Coordinate) -> bool:
        starting_index = self.gui.traverse_layers().index(self) + 1
        return not any(layer.is_occupied_at(at) for layer in self.gui.traverse_layers(start=starting_index))

    def new_character_on_erase_at(self, at: Coordinate) -> SupportsString | None:
        if not self.can_print_at(at):
            return
        starting_index = self.gui.n_layers - self.gui.traverse_layers().index(self)
        for layer in self.gui.traverse_layers(start=starting_index, reverse=True):
            if layer.is_occupied_at(at):
                return layer.content[at]
        return self.gui.ERASE_CHARACTER

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

    def __lt__(self, other: Layer) -> bool:
        return self.z <= other.z
