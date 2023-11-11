# noinspection PyProtectedMember
from threading import ThreadError, Thread, _active
from ctypes import pythonapi, c_long, py_object


class KillableThread(Thread):
    def __init__(self, *args: object, **kwargs: object) -> None:
        super().__init__(*args, **kwargs)

    def get_id(self):
        if not self.is_alive():
            raise ThreadError("Thread not active") from None
        for id_, obj in _active.items():
            if obj is self:
                return id_
        raise AssertionError("Could not determine thread ID") from None

    def kill(self):
        thread_id = self.get_id()
        code = pythonapi.PyThreadState_SetAsyncExc(c_long(thread_id), py_object(ThreadError))
        if not code:
            raise ValueError("Invalid thread ID") from None
        elif code != 1:
            pythonapi.PyThreadState_SetAsyncExc(c_long(thread_id), None)
            raise SystemError("PyThreadState_SetAsyncExc failed") from None
