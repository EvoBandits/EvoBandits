class Bounds:
    def __init__(self) -> None:
        self.low = []
        self.high = []

    @property
    def as_tuples(self) -> list:
        as_tuple = [(self.low[idx], self.high[idx]) for idx in range(len(self.low))]
        return as_tuple

    def suggest_int(self, low: int, high: int, size: int = 1) -> None:
        if not all(isinstance(var, int) for var in [low, high, size]):
            raise TypeError("low, high, size must be integers when suggesting an int.")
        if high <= low:
            raise ValueError("high must be larger than low when suggesting an int.")
        if size <= 0:
            raise ValueError("size must be positive when suggesting an int.")
        for _ in range(size):
            self.low.append(low)
            self.high.append(high)
