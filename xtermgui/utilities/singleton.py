class Singleton[T, ** P](type):
    __slots__ = ()
    _instances: dict[type[T], T] = {}

    def __call__(cls, *args: P.args, **kwargs: P.kwargs) -> T:
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
