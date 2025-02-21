class IntParam:
    """
    A class representing an integer parameter.
    """

    def __init__(self, low: int, high: int, size: int = 1, step: int = 1):
        """
        Construct a  instance of IntParam.

        Args:
            low (int): A valid lower bound of the parameter.
            high (int): A valid upper bound of the parameter.
            size (int): A valid, positive size of the parameter. Default is 1.
            step (int): A valid, positive step size for the parameter. Default is 1.

        """
        self.low: int = low
        self.high: int = high
        self.size: int = size
        self.step: int = step
        self._bounds: list[tuple] | None = None

    @property
    def bounds(self) -> list[tuple]:
        """
        Calculate and return the parameter's internal bounds for the optimization.

        The bounds will be used as constraints for the internal representation (or actions)
        of the optimization algorithm about the parameter's value.

        Returns:
            list[tuple]: A list of tuples representing the bounds.

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

    def map_to_value(self, actions: list[int]) -> int | list[int]:
        """
        Maps a single set of internal actions for this parameter to its value.

        Args:
            actions (list[int]): A list of integers to map.

        Returns:
            int | list[int]: The resulting value.
        """
        if self.step > 1:
            actions = [min(self.low + x * self.step, self.high) for x in actions]

        if self.size == 1:
            return actions[0]
        return actions


def suggest_int(low: int, high: int, size: int = 1, step: int = 1) -> IntParam:
    """
    Creates an integer parameter to suggest values for the optimization.

    The parameter can be either a simple integer, or a list of integers, depending on the specified
    size. The values that can be sampled by the optimization will be limited to the specified
    lower and upper bound, as well as the stepsize.

    Args:
        low (int): The lower bound of the parameter.
        high (int): The upper bound of the parameter.
        size (int): The size of the parameter, if it should be list. Default is 1.
        step (int): The step size for the parameter. Default is 1.

    Returns:
        IntParam: An instance of the parameter with the specified properties.

    Raises:
        TypeError: If any of the arguments are not integers.
        ValueError: If high is not greater than low, or if size or step is not positive.
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
