class Bounds:
    def __init__(self) -> None:
        self.low = []
        self.high = []

    @property
    def as_tuples(self) -> list:
        as_tuple = [(self.low[idx], self.high[idx]) for idx in range(len(self.low))]
        return as_tuple

    def suggest_int(self, low: int, high: int, size: int = 1) -> None:
        # Add checks if low, high, size are valid
        if high <= low:
            raise ValueError(f"high={high} must be > low={low} when suggesting an int.")

        for _ in range(size):
            self.low.append(low)
            self.high.append(high)
