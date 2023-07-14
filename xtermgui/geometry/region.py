from dataclasses import dataclass, field
from .coordinate import Coordinate


@dataclass(frozen=True, slots=True, init=False)
class Region:
    vertices: tuple[Coordinate] = field(init=False)
    n_vertices: int = field(init=False)

    def __init__(self, *vertices: Coordinate):
        object.__setattr__(self, "n_vertices", len(vertices))
        if self.n_vertices < 3:
            raise ValueError("Region cannot be formed from less than 3 coordinates.") from None
        object.__setattr__(self, "vertices", vertices)

    def __contains__(self, coordinate: Coordinate):  # https://wrfranklin.org/Research/Short_Notes/pnpoly.html
        contains = False
        for end, start in zip(self.vertices, (self.vertices[-1], *self.vertices[:-1])):
            if (
                    ((end.y > coordinate.y) != (start.y > coordinate.y)) and
                    (coordinate.x < (start.x - end.x) * (coordinate.y - end.y) / (start.y - end.y) + end.x)
            ):
                contains = not contains
        return contains
