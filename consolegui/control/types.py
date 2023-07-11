from typing import Protocol, Any


class SupportsLessThan(Protocol):
    def __lt__(self, other: Any) -> bool:
        ...


class SupportsString(Protocol):
    def __str__(self) -> str:
        ...
