from gmab.utils.singleton import Singleton


class Trial(Singleton):
    """A singleton class that manages bounds for trials with the objective function.

    This class is designed to handle and store trial parameters, including their names,
    lower bounds, and upper bounds. It also computes parameter bounds when requested.
    The singleton pattern ensures there is only one instance of this class,
    which is useful for consistent trial management across a study.

    """

    def __init__(self):
        if not hasattr(self, "_names"):
            self._names: list = []
        if not hasattr(self, "low"):
            self._low: list = []
        if not hasattr(self, "_high"):
            self._high: list = []
        if not hasattr(self, "_bounds"):
            self._bounds: list[tuple] | None = None

    @classmethod
    def reset(cls):
        """Reset the Trial singleton instance without performing cleanup.

        This method removes the existing singleton instance, allowing a new instance
        to be created the next time the class is instantiated, but keeping the bounds
        stored in this instances for later use.
        """
        super().reset()

    @property
    def bounds(self) -> list[tuple]:
        """Computes and returns the list of parameter bounds.

        Returns:
            list[tuple]: A list of tuples representing parameter bounds, where each
            tuple is (low, high) for a parameter.
        """
        if not self._bounds:
            bounds = []
            for idx in range(len(self._names)):
                bounds.append((self._low[idx], self._high[idx]))
            self._bounds = bounds
        return self._bounds

    def suggest_int(self, name: str, low: int, high: int, size: int = 1) -> None:
        """Suggest a value for the integer parameter.

        Args:
            name:
                A parameter name.
            low:
                Lower endpoint of the range of suggested values.
            high:
                Upper endpoint of the range of suggested values.

        """
        for idx in range(size):
            self._names.append(f"{name}_{idx}")
            self._low.append(low)
            self._high.append(high)


# Instantiate Trial in the module to replicate Optuna's behaviour
trial = Trial()
