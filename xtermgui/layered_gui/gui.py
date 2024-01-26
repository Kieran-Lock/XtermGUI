from __future__ import annotations

from contextlib import contextmanager
from copy import copy
from dataclasses import dataclass, field
from heapq import heappush, nlargest, nsmallest, heapify
from sys import stdout
from typing import Callable, Iterator

from .layer import Layer
from ..control import Cursor, Text
from ..geometry import Coordinate
from ..gui import GUI
from ..utilities import SupportsString


@dataclass(slots=True)
class LayeredGUI(GUI):
    base_layer_name: str = "Base"
    _layers: list[Layer] = field(default_factory=list, init=False)
    base_layer: Layer = field(init=False, default=None)
    active_layer: Layer = field(init=False, default=None)
    n_layers: int = field(init=False, default=0)

    def __post_init__(self) -> None:
        super(LayeredGUI, self).__post_init__()
        self.base_layer = self.add_layer(self.base_layer_name, 0)
        self.active_layer = self.base_layer

    def print(self, *text: SupportsString, sep: SupportsString = ' ', end: SupportsString = "", flush: bool = True,
              at: Coordinate | None = None, layer: Layer | None = None, force: bool = False) -> None:
        if at is not None:
            Cursor.go_to(at)
        else:
            at = Cursor.position
        if layer is None:
            layer = self.active_layer
        string = str(sep).join(map(str, text)) + str(end)
        if not string:
            return
        for index, (character, cursor_position) in enumerate(Text.cursor_print_displacement(string)):
            if force or layer.can_print_at(at):  # TODO: Fix this
                if character != Text.TRANSPARENT:  # TODO: Text constants migration
                    layer.write(character, at=cursor_position)
            else:
                string = string[:index] + Text.TRANSPARENT + string[index + 1:]
        print(string, end="", flush=flush)
        Cursor.sync_position()

    def print_inline(self, *text: SupportsString, sep: SupportsString = ' ', end: SupportsString = "",
                     flush: bool = True, at: Coordinate | None = None, layer: Layer | None = None,
                     force: bool = False) -> None:
        if at is not None:
            Cursor.go_to(at)  # TODO: Look at efficiency
        result = str(sep).join(map(str, text)) + str(end)
        initial_x = Cursor.position.x
        for i, string in enumerate(result.split('\n')):
            y = Cursor.position.y + 1 if i else Cursor.position.y
            self.print(string, flush=False, at=Coordinate(initial_x, y), layer=layer, force=force)
        if flush:
            stdout.flush()

    def erase(self, at: Coordinate | None = None, flush: bool = True, layer: Layer | None = None,
              force: bool = False) -> None:
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
        if not self.n_layers:
            return Coordinate(0, 0)
        sizes = set(layer.get_size() for layer in self._layers)
        return Coordinate(
            max(size.x for size in sizes),
            max(size.y for size in sizes),
        )

    def add_layer(self, name: str, z: float | None = None) -> Layer:
        if z is None:
            z = max(self._layers).z
        layer = Layer(self, name, z)
        heappush(self._layers, layer)
        self.n_layers += 1
        return layer

    def get_layers(self, predicate: Callable[[Layer], bool]) -> Layer:
        return (layer for layer in self.traverse_layers() if predicate(layer))

    def remove_layers(self, predicate: Callable[[Layer], bool]) -> Iterator[Layer]:
        for i, layer in enumerate(self._layers):
            if predicate(layer):
                self.n_layers -= 1
                yield self._layers.pop(i)
        heapify(self._layers)

    def traverse_layers(self, start: int = 0, end: int | None = None, reverse: bool = False) -> list[Layer]:
        if end is None:
            end = self.n_layers
        layers = nlargest(end, self._layers) if reverse else nsmallest(end, self._layers)
        return layers[start:] if start else layers

    def clear(self, layer: Layer | None = None) -> None:
        if layer is None:
            super(LayeredGUI, self).clear()
            for layer in self._layers:
                layer.clear_content()
            return
        for coordinate in copy(layer.content):
            self.erase(at=coordinate, layer=layer)

    @contextmanager
    def remember_active_layer(self) -> None:
        previous_active_layer = self.active_layer
        try:
            yield
        finally:
            self.active_layer = previous_active_layer
