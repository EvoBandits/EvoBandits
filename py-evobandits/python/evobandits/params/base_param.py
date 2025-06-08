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

from abc import ABC, abstractmethod
from collections.abc import Callable


class BaseParam(ABC):
    """
    An abstract base class representing a parameter in an optimization problem.

    This class defines the interface for parameters that suggest values during
    optimization. Subclasses must implement the `bounds` property and the
    `map_to_value` method to define how the parameter's bounds are calculated
    and how actions are mapped to parameter values for the objective function.
    The `size` attribute determines the dimensionality of the parameter.
    """

    def __init__(self, size: int = 1) -> None:
        """
        Initializes a BaseParam instance.

        Args:
            The size of the parameter if it is a list. This determines
            the number of dimensions for the parameter. Defaults to 1.

        Raises:
            ValueError: If size is not a positive integer.
        """
        if size < 1:
            raise ValueError("size must be a positive integer.")
        self.size: int = int(size)

    @property
    @abstractmethod
    def bounds(self) -> list[tuple[int, int]]:
        """
        Abstract property to calculate and return the parameter's internal bounds.

        The bounds are used as constraints for the optimization algorithm's
        internal representation of the parameter's value. Subclasses must
        implement this property to provide the specific bounds for the parameter,
        taking into account the `size`.

        Returns:
            A list of tuples representing the bounds, where each tuple
            contains the lower and upper bounds for a dimension. The length of the
            list should match the `size`.

        """
        raise NotImplementedError("Subclasses must implement the 'bounds' property.")

    @abstractmethod
    def decode(self, actions: list[int]) -> bool | int | str | float | Callable | None | list:
        """
        Abstract method to decode optimization actions as parameter values.

        This method converts a list of integers (actions) into the corresponding
        parameter value(s). Subclasses must implement this method to define the
        specific mapping logic, considering the `size`.

        Args:
            actions: A list of integers representing actions from the
            optimization algorithm. The length of this list should match the `size`.

        Returns:
            The resulting parameter value(s) corresponding to the given actions.
            Returns the value directly in case of `self.size` equals 1, a list of values else.
        """
        raise NotImplementedError("Subclasses must implement the 'map_to_value' method.")
