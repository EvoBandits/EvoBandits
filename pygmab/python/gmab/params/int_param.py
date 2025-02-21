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
            self._bounds = [(self.low, self.high)] * self.size
        return self._bounds

    def map(self, numbers: list[int]) -> list[int]:
        """
        ToDo
        """
        if len(numbers) == 1:
            return numbers[0]
        return numbers


class SteppedIntParam(IntParam):
    def __init__(self, low: int, high: int, size: int = 1, step: int = 1):
        """
        ToDo
        """
        super().__init__(low, high, size)
        self.step: int = step

    @property
    def bounds(self) -> list[tuple]:
        """
        ToDo
        """
        if not self._bounds:
            n_steps = (self.high - self.low) // self.step
            n_steps += 1 if (self.high - self.low) % self.step != 0 else 0
            self._bounds = [(0, n_steps)] * self.size
        return self._bounds

    def map(self, numbers: list[int]) -> list[int]:
        """
        ToDo
        """
        mapping = [min(self.low + x * self.step, self.high) for x in numbers]
        if len(mapping) == 1:
            return mapping[0]
        return mapping


def suggest_int(low: int, high: int, size: int = 1, step: int = 1) -> IntParam:
    """
    ToDo
    """
    if not all(isinstance(args, int) for args in [low, high, size, step]):
        raise TypeError("low, high, size and step must be int when suggesting an integer param.")
    if high <= low:
        raise ValueError("high must be larger than low when suggesting an integer param.")
    if size < 1:
        raise ValueError("size must be positive when suggesting an integer param.")
    if step < 1:
        raise ValueError("step must be positive when suggesting an integer param.")

    if step != 1:
        return SteppedIntParam(low, high, size, step)
    return IntParam(low, high, size)
