from typing import Protocol


class SupportsString(Protocol):
    def __str__(self) -> str:
        ...
