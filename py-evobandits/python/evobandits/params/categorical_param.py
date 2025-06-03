# Copyright 2025 EvoBandits
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from collections.abc import Callable

from evobandits.params.base_param import BaseParam

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

    @property
    def bounds(self) -> list[tuple]:
        """
        Calculates and returns the parameter's internal bounds for optimization.

        The bounds are used as constraints for the internal representation (or actions)
        of the optimization algorithm regarding the parameter's value.

        Returns:
            list[tuple]: A list of tuples representing the bounds.
        """
        return [(0, len(self.choices) - 1)]

    def decode(self, actions: list[int]) -> ChoiceType | list[ChoiceType]:
        """
        Decodes an action from the optimization problem to the value of the parameter.

        Args:
            actions (list[int]): A list of integers to map.

        Returns:
            ChoiceType | list[ChoiceType]: The resulting choice(s).
        """
        actions = [self.choices[idx] for idx in actions]

        if len(actions) == 1:
            return actions[0]
        return actions
