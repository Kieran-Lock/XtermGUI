from __future__ import annotations
from contextlib import contextmanager
from typing import Callable, Iterator
from dataclasses import dataclass, field
from heapq import heappush, nlargest, nsmallest
from copy import copy
from .layer import Layer
from ..gui import GUI
from ..geometry import Coordinate
from ..control import Cursor, SupportsString, SupportsLessThan


@dataclass(slots=True)
class LayeredGUI(GUI):
    base_layer_name: str = "Base"
    layers: list[Layer | SupportsLessThan] = field(default_factory=list, init=False)
    base_layer: Layer = field(init=False)
    active_layer: Layer = field(init=False)

    def __post_init__(self) -> None:
        super(LayeredGUI, self).__post_init__()
        self.base_layer = self.add_layer(self.base_layer_name, 0)
        self.active_layer = self.base_layer

    def print(self, *text: SupportsString, sep: SupportsString = " ", end: SupportsString = "", flush: bool = True, at: Coordinate | None = None, layer: Layer | None = None, force: bool = False) -> None:
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
            Cursor.update_position_on_print(character)

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
        Cursor.update_position_on_print(self.__class__.ERASE_CHARACTER)

    def get_size(self) -> Coordinate:
        return max(map(lambda layer: layer.get_size(), self.layers))

    def add_layer(self, name: str, z: float | None = None) -> Layer:
        if z is None:
            z = max(self.layers).z
        layer = Layer(self, name, z)
        heappush(self.layers, layer)
        return layer

    def get_layer(self, key: Callable[[Layer], bool]) -> Layer:
        return next(layer for layer in self.layers if key(layer))

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
