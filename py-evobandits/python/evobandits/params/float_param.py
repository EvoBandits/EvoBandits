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

import math

from evobandits.params.base_param import BaseParam


class FloatParam(BaseParam):
    """
    A class representing a float parameter.
    """

    def __init__(
        self, low: float, high: float, size: int = 1, n_steps: float = 100, log: bool = False
    ) -> None:
        """
        Creates a FloatParam that will suggest float values during the optimization.

        The parameter can either be a float, or a list of floats, depending on the specified
        size. The values sampled by the optimization will be limited to the specified granularity,
        lower and upper bounds.

        Args:
            low: The lower bound of the suggested values.
            high: The upper bound of the suggested values.
            size: The size if the parameter shall be a list of floats. Default is 1.
            n_steps: The number of steps between low and high. Default is 100.
            log: A flag to indicate log-transformation. Default is False.

        Returns:
            FloatParam: An instance of the parameter with the specified properties.

        Raises:
            ValueError: If low is not an float, if high is not an float that is greater than
            low, or if size is not a positive integer, or if step is not a positive float.

        Example:
        >>> param = FloatParam(low=1.0, high=10.0, size=3, n_steps=100)
        >>> print(param)
        FloatParam(low=1.0, high=10.0, size=3, n_steps=100)
        """
        if high <= low:
            raise ValueError("high must be a float that is greater than low.")
        if n_steps <= 0:
            raise ValueError("steps must be positive integer.")
        if log and low <= 0.0:
            raise ValueError("low must be greater than 0 for a log-transformation.")

        super().__init__(size)
        self.log: bool = bool(log)
        self.low: float = float(low)
        self.high: float = float(high)
        self.n_steps: int = int(n_steps)

    def __repr__(self) -> str:
        repr = f"FloatParam(low={self.low}, high={self.high}, size={self.size}, "
        repr += f"n_steps={self.n_steps}, log={self.log})"
        return repr

    @property
    def _low_trans(self) -> float:
        if self.log:
            return math.log(self.low)
        return self.low

    @property
    def _step_size(self) -> float:
        high_trans = math.log(self.high) if self.log else self.high
        return (high_trans - self._low_trans) / self.n_steps

    @property
    def bounds(self) -> list[tuple[int, int]]:
        """
        Calculate and return the parameter's internal bounds for the optimization.

        The bounds will be used as constraints for the internal representation (or actions)
        of the optimization algorithm about the parameter's value

        Returns:
            A list of tuples representing the bounds
        """
        return [(0, self.n_steps)] * self.size

    def decode(self, actions: list[int]) -> float | list[float]:
        """
        Decodes an action by the optimization problem to the value of the parameter.

        Args:
            A list of integer to map.

        Returns:
            The resulting float value(s).
        """
        # Apply scaling
        values = [self._low_trans + self._step_size * x for x in actions]

        # Optional log-transformation
        if self.log:
            values = [math.exp(x) for x in values]

        if len(values) == 1:
            return values[0]
        return values
