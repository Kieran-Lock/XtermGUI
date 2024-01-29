from __future__ import annotations

from contextlib import contextmanager
from copy import copy
from dataclasses import dataclass, field
from heapq import heappush, nlargest, nsmallest, heapify
from typing import Callable, Iterator

from .layer import Layer
from ..geometry import Coordinate
from ..gui import GUI
from ..terminal import terminal
from ..text import Text, Characters, AnsiEscapeSequence
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

    def print(self, *values: SupportsString, sep: SupportsString = ' ', end: SupportsString = "", flush: bool = True,
              at: Coordinate | None = None, layer: Layer | None = None) -> None:
        if at is not None:
            terminal.cursor.go_to(at)
        else:
            at = terminal.cursor.position
        if layer is None:
            layer = self.active_layer
        text = Text.as_printed(*values, sep=sep, end=end)
        if not text:
            return
        cursor_position = at
        offset = 0
        from log import log
        for character_info, cursor_position in terminal.cursor.get_print_displacement(text):
            index = character_info.index + offset
            if not isinstance(character_info.character, AnsiEscapeSequence):
                layer.write(character_info.character, at=cursor_position)  # TODO: Still writes other characters like \n
            if not layer.can_print_at(cursor_position):
                text = text.replace_at(index, Characters.TRANSPARENT, n=len(character_info.character))
                offset += 3
        print(text, end="", flush=flush)
        log("[PRINTING]", text)
        terminal.cursor.go_to(cursor_position)

    def print_inline(self, *values: SupportsString, sep: SupportsString = ' ', end: SupportsString = "",
                     flush: bool = True, at: Coordinate | None = None, layer: Layer | None = None) -> None:
        if at is not None:
            terminal.cursor.go_to(at)
        initial_x = terminal.cursor.position.x
        text = (Text.as_printed(*values, sep=sep, end=end)
                .replace(Characters.NEWLINE, f"{Characters.NEWLINE}{Characters.TRANSPARENT * initial_x}"))
        self.print(text, end="", flush=flush, at=at, layer=layer)

    def erase(self, at: Coordinate | None = None, flush: bool = True, layer: Layer | None = None,
              force: bool = False) -> None:
        if at is not None:
            terminal.cursor.go_to(at)
        else:
            at = terminal.cursor.position
        if layer is None:
            layer = self.active_layer
        if force:
            print(self.__class__.ERASE_CHARACTER, end="", flush=flush)
        elif (new_character := layer.new_character_on_erase_at(at)) is not None:
            print(new_character, end="", flush=flush)
        layer.erase_content(at=at)
        terminal.cursor.sync_position()

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
