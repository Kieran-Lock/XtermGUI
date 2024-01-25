from typing import Iterator
from contextlib import contextmanager


class InputLock:
    current_priority: float = 0

    @classmethod
    @contextmanager
    def acquire(cls, priority: float = 1) -> Iterator[None]:
        if not cls.can_acquire(priority):  # TODO: Implement threading locks
            raise ValueError(
                f"Process attempted to acquire lock for read from stdin without sufficient priority ({priority=} < {cls.current_priority=}).")
        old_priority = cls.current_priority
        cls.current_priority = priority
        try:
            yield
        finally:
            cls.current_priority = old_priority

    @classmethod
    def can_acquire(cls, priority: float) -> bool:
        return priority > cls.current_priority
