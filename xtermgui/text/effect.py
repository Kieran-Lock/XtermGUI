from __future__ import annotations

from abc import abstractmethod
from dataclasses import dataclass


@dataclass(frozen=True, slots=True, kw_only=True)
class Effect:
    @property
    @abstractmethod
    def escape_sequence_segment(self) -> str:
        ...

    @abstractmethod
    def __contains__(self, effect: Effect) -> bool:
        ...
