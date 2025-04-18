from collections.abc import Callable
from functools import cached_property

from gmab.params.base_param import BaseParam

ChoiceType = bool | int | float | str | Callable | None


class CategoricalParam(BaseParam):
    """
    A class representing a categorical parameter.
    """

    def __init__(self, choices: list[ChoiceType]):
        """
        Creates a CategoricalParam that will suggest one of the choices during optimization.

        Args:
            choices (list[ChoiceType]): A list of possible choices for the parameter.

        Returns:
            CategoricalParam: An instance of the parameter with the specified properties.

        Raises:
            ValueError: Raises a ValueError if choices is not a list, or if the objects in the list
            are not of an immutable or callable type (bool, int, float, str, Callable, or None).
            For example, a list of dictionaries or lists would raise an error.

        Example:
        >>> param = CategoricalParam(choices=["a", "b", "c"])
        >>> print(param)
        CategoricalParam(["a", "b", "c"])

        Note:
            This parameter assumes an ordinal scale for the choices during optimization.
        """
        if not isinstance(choices, list):
            raise ValueError("choices must be a list")
        if not all(isinstance(c, ChoiceType) for c in choices):
            raise ValueError("All elements in choices must be of an immutable or callable type")

        super().__init__(size=1)
        self.choices: list[ChoiceType] = choices

    def __repr__(self):
        return f"CategoricalParam(choices={self.choices})"

    @cached_property
    def bounds(self) -> list[tuple]:
        """
        Calculates and returns the parameter's internal bounds for optimization.

        The bounds are used as constraints for the internal representation (or actions)
        of the optimization algorithm regarding the parameter's value.

        Returns:
            list[tuple]: A list of tuples representing the bounds.
        """
        return [(0, len(self.choices) - 1)]

    def map_to_value(self, actions: list[int]) -> ChoiceType | list[ChoiceType]:
        """
        Maps an action from the optimization problem to the value of the parameter.

        Args:
            actions (list[int]): A list of integers to map.

        Returns:
            ChoiceType | list[ChoiceType]: The resulting choice(s).
        """
        actions = [self.choices[idx] for idx in actions]

        if len(actions) == 1:
            return actions[0]
        return actions
