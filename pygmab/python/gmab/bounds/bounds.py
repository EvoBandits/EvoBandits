class Bounds:
    """The Bounds module manages the user-configured boundaries for gmab.

    This object provides interfaces to set the bounds that will be suggested
    for the optimization.
    """

    def __init__(self) -> None:
        self.low = []
        self.high = []

    @property
    def internal(self) -> list[tuple]:
        """Creates and returns the internal bounds for gmab.

        Returns:
            list[tuple]: A list of tuples, containaing a (low, high) pair for each bound.
        """
        as_tuple = [(self.low[idx], self.high[idx]) for idx in range(len(self.low))]
        return as_tuple

    def suggest_int(self, low: int, high: int, size: int = 1) -> None:
        """Adds an integer decision parameter to the bounds.

        Args:
            low (int): The lower bound of the parameter.
            high (int): The upper bound of the parameter.
            size (int, optional): Length of the decision vector, defaults to 1.

        Raises:
            TypeError: If low, high, or size are not integers.
            ValueError: If high <= low or size non-positive.
        """
        if not all(isinstance(var, int) for var in [low, high, size]):
            raise TypeError("low, high, size must be integers when suggesting an int.")
        if high <= low:
            raise ValueError("high must be larger than low when suggesting an int.")
        if size <= 0:
            raise ValueError("size must be positive when suggesting an int.")
        for _ in range(size):
            self.low.append(low)
            self.high.append(high)
