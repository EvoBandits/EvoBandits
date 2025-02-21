class IntParam:
    """
    ToDo
    """

    def __init__(self, low: int, high: int, size: int = 1):
        """
        ToDo
        """
        self.low: int = low
        self.high: int = high
        self.size: int = size

        self._bounds: list[tuple] | None = None

    @property
    def bounds(self) -> list[tuple]:
        """
        ToDo
        """
        if not self._bounds:
            # bounds = []
            # for _ in range(self.size):
            #     bounds.append((self.low, self.high))
            # self._bounds = bounds
            self._bounds = [(self.low, self.high)] * self.size
        return self._bounds


def suggest_int(low: int, high: int, size: int = 1) -> IntParam:
    """
    ToDo
    """
    if not all(isinstance(args, int) for args in [low, high, size]):
        raise TypeError("low, high and size must be int when suggesting an integer param.")
    if high <= low:
        raise ValueError("high must be larger than low when suggesting an integer param.")
    if size < 1:
        raise ValueError("size must be positive when suggesting an integer param.")

    return IntParam(low, high, size)
