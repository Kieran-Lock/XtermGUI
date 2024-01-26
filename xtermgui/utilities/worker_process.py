from threading import current_thread
from multiprocessing import Process
from signal import pause, signal, SIGCONT, SIGUSR1
from typing import Callable
from types import FrameType
from os import kill


class WorkerProcess[**P, R](Process):
    def __init__(
        self,
        target: Callable[P, R],
        name: str | None = None,
        args: P.args = (),
        kwargs: P.kwargs = None,
        *,
        daemon: bool | None = None,
        debug: bool = False,
    ) -> None:
        super().__init__(
            target=target,
            name=name,
            args=args,
            kwargs=kwargs if kwargs else {},
            daemon=daemon
        )
        self.paused = False
        self.debug = debug
        signal(SIGUSR1, self._pause_signal_handler)
        signal(SIGCONT, self._resume_signal_handler)

    def _pause_signal_handler(self, signal_number: int, _: FrameType) -> None:
        if self.debug:
            print(f"[WORKER] Received PAUSE signal {signal_number} in thread: {current_thread().ident}")
        pause()

    def _resume_signal_handler(self, signal_number: int, _: FrameType) -> None:
        if self.debug:
            print(f"[WORKER] Received RESUME signal {signal_number} in thread: {current_thread().ident}")

    def pause(self) -> None:
        if self.debug:
            print(f"[MAIN] Pausing process {self.pid} from thread {current_thread().ident}!")
        kill(self.pid, SIGUSR1)
        self.paused = True

    def resume(self) -> None:
        if self.debug:
            print(f"[MAIN] Resuming process {self.pid} from thread {current_thread().ident}!")
        kill(self.pid, SIGCONT)
        self.paused = False
