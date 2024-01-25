from __future__ import annotations

from contextlib import contextmanager
from typing import Callable, Iterator
from dataclasses import dataclass, field
from heapq import heappush, nlargest, nsmallest
from copy import copy
from sys import stdout

from .layer import Layer
from ..gui import GUI
from ..geometry import Coordinate
from ..control import Cursor
from ..utilities import SupportsString, SupportsLessThan


@dataclass(slots=True)
class LayeredGUI(GUI):
    base_layer_name: str = "Base"
    layers: list[Layer | SupportsLessThan] = field(default_factory=list, init=False)
    base_layer: Layer = field(init=False, default=None)
    active_layer: Layer = field(init=False, default=None)

    def __post_init__(self) -> None:
        super(LayeredGUI, self).__post_init__()
        self.base_layer = self.add_layer(self.base_layer_name, 0)
        self.active_layer = self.base_layer

    def print(self, *text: SupportsString, sep: SupportsString = ' ', end: SupportsString = "", flush: bool = True, at: Coordinate | None = None, layer: Layer | None = None, force: bool = False) -> None:
        if at is not None:
            Cursor.go_to(at)
        else:
            at = Cursor.position
        if layer is None:
            layer = self.active_layer
        if force or layer.can_print_at(at):
            print(*text, sep=str(sep), end=str(end), flush=flush)
        for character in str(sep).join(map(str, text)) + str(end):
            layer.write(character, at=Cursor.position)
        Cursor.sync_position()

    def print_inline(self, *text: SupportsString, sep: SupportsString = ' ', end: SupportsString = "", flush: bool = True, at: Coordinate | None = None, layer: Layer | None = None, force: bool = False) -> None:
        if at is not None:
            Cursor.go_to(at)
        result = str(sep).join(map(str, text)) + str(end)
        initial_x = Cursor.position.x
        for i, string in enumerate(result.split('\n')):
            y = Cursor.position.y + 1 if i else Cursor.position.y
            self.print(string, flush=False, at=Coordinate(initial_x, y), layer=layer, force=force)
        if flush:
            stdout.flush()

    def erase(self, at: Coordinate | None = None, flush: bool = True, layer: Layer | None = None, force: bool = False) -> None:
        if at is not None:
            Cursor.go_to(at)
        else:
            at = Cursor.position
        if layer is None:
            layer = self.active_layer
        if force:
            print(self.__class__.ERASE_CHARACTER, end="", flush=flush)
        elif (new_character := layer.new_character_on_erase_at(at)) is not None:
            print(new_character, end="", flush=flush)
        layer.erase_content(at=at)
        Cursor.sync_position()

    def get_size(self) -> Coordinate:
        sizes = set(layer.get_size() for layer in self.layers)
        return Coordinate(
            max(size.x for size in sizes),
            max(size.y for size in sizes),
        )

    def add_layer(self, name: str, z: float | None = None) -> Layer:
        if z is None:
            z = max(self.layers).z
        layer = Layer(self, name, z)
        heappush(self.layers, layer)
        return layer

    def get_layer(self, predicate: Callable[[Layer], bool]) -> Layer:
        return next(layer for layer in self.layers if predicate(layer))

    def remove_layer(self, name: str) -> None:
        self.layers = list(filter(lambda layer: layer.name == name, self.layers))

    def traverse_layers(self, start: int = 0, end: int | None = None, reverse: bool = False):
        if end is None:
            layers = list(reversed(self.layers)) if reverse else self.layers
        else:
            n = end - start
            layers = nlargest(n, self.layers) if reverse else nsmallest(n, self.layers)
        return (layer for layer in layers[start:])

    def clear(self, layer: Layer | None = None) -> None:
        if layer is None:
            super(LayeredGUI, self).clear()
            for layer in self.layers:
                layer.clear_content()
            return
        for coordinate in copy(layer.content):
            self.erase(at=coordinate, layer=layer)

    @contextmanager
    def as_active(self, layer: Layer) -> Iterator[Layer]:
        previous_active_layer = self.active_layer
        self.active_layer = layer
        try:
            yield layer
        finally:
            self.active_layer = previous_active_layer
