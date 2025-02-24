from abc import ABC, abstractmethod


class BaseParam(ABC):
    def __init__(self, size: int = 1):
        if not isinstance(size, int) or size < 1:
            raise ValueError("size must be a positive integer.")
        self.size: int = size
        self._bounds: list[tuple] | None = None

    @property
    @abstractmethod
    def bounds(self) -> list[tuple]:
        """
        Calculate and return the parameter's internal bounds for the optimization.

        The bounds will be used as constraints for the internal representation (or actions)
        of the optimization algorithm about the parameter's value.

        Returns:
            list[tuple]: A list of tuples representing the bounds.

        """
        if not self._bounds:
            raise NotImplementedError
        return self._bounds

    @abstractmethod
    def map_to_value(self, actions: list[int]) -> bool | int | str | float | list:
        """
        Maps an action by the optimization problem to the value of the parameter.

        Args:
            actions (list[int]): A list of integers to map.

        Returns:
            int | list[int]: The resulting value(s).
        """
        raise NotImplementedError
