from __future__ import annotations
from typing import Callable
from dataclasses import dataclass, field
from heapq import heappush, nlargest, nsmallest
from .layer import Layer
from ..gui import GUI
from ..geometry import Coordinate
from ..control import Cursor, SupportsString


DEBUG_Y = 20


@dataclass(slots=True)
class LayeredGUI(GUI):
    base_layer_name: str = "Base"
    layers: list[Layer] = field(default_factory=list, init=False)
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
            print(*text, sep=sep, end=end, flush=flush)
        for character in str(sep).join(map(str, text)):
            layer.write(character, at=Cursor.position)
            Cursor.update_position_on_print(character)

    def erase(self, at: Coordinate | None = None, layer: Layer | None = None, force: bool = False) -> None:
        if at is not None:
            Cursor.go_to(at)
        else:
            at = Cursor.position
        if layer is None:
            layer = self.active_layer
        if force or (new_character := layer.new_character_on_erase_at(at)) is not None:
            if force:
                new_character = self.__class__.ERASE_CHARACTER
            print(new_character, end="", flush=True)
        layer.erase(at=at)
        Cursor.update_position_on_print(self.__class__.ERASE_CHARACTER)

    def get_size(self) -> Coordinate:
        self.layers = self.layers
        return Coordinate(0, 0)

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

    def debug(self, *text: SupportsString) -> None:
        global DEBUG_Y
        old_position = Cursor.position
        self.print(*text, at=Coordinate(0, DEBUG_Y), force=True)
        DEBUG_Y += 1
        Cursor.go_to(old_position)

    def clear(self) -> None:
        super(LayeredGUI, self).clear()
        for layer in self.layers:
            layer.clear()
