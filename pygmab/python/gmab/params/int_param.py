class IntParam:
    """
    ToDo
    """

    def __init__(self, low: int, high: int, size: int = 1, step: int = 1):
        """
        ToDo
        """
        self.low: int = low
        self.high: int = high
        self.size: int = size
        self.step: int = step
        self._bounds: list[tuple] | None = None

    @property
    def bounds(self) -> list[tuple]:
        """
        ToDo
        """
        if not self._bounds:
            if self.step == 1:
                upper_bound = self.high
            else:
                upper_bound = (self.high - self.low) // self.step
                upper_bound += 1 if (self.high - self.low) % self.step != 0 else 0
                upper_bound += self.low
            self._bounds = [(self.low, upper_bound)] * self.size
        return self._bounds

    def map(self, numbers: list[int]) -> int | list[int]:
        """
        ToDo
        """
        if self.step > 1:
            numbers = [min(self.low + x * self.step, self.high) for x in numbers]

        if self.size == 1:
            return numbers[0]
        return numbers


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

    return IntParam(low, high, size, step)
