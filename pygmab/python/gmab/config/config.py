class Configurator:
    """Manages the user's configuration of the objective.

    This object provides interfaces to define the configuration that will be suggested
    for the optimization of the Study.
    """

    def __init__(self) -> None:
        self.low: list[int] = []
        self.high: list[int] = []
        self._bounds: list[tuple] | None = None

    @property
    def bounds(self) -> list[tuple]:
        """Returns the (cached) bounds for rust-gmab.

        Returns:
            list[tuple]: A list of tuples, containing a (low, high) pair for each bound.
        """
        if not self._bounds:
            self._bounds = [(self.low[idx], self.high[idx]) for idx in range(len(self.high))]
        return self._bounds

    def suggest_int(self, low: int, high: int, size: int = 1) -> None:
        """Sets up the configuration to suggest integer values for the decision parameter.

        Args:
            low (int): The lower bound of the parameter.
            high (int): The upper bound of the parameter.
            size (int, optional): Length, if parameter is a vector. Defaults to 1.

        Raises:
            TypeError: If low, high, or size are not integers.
            ValueError: If high <= low or size non-positive.
        """
        if not all(isinstance(var, int) for var in [low, high, size]):
            raise TypeError("low, high, size must be integers when suggesting an int.")
        if high <= low:
            raise ValueError("high must be larger than low when suggesting an int.")
        if size < 1:
            raise ValueError("size must be positive when suggesting an int.")

        for _ in range(size):
            self.low.append(low)
            self.high.append(high)
