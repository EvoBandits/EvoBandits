from collections.abc import Callable, Mapping
from typing import TypeAlias

from evobandits import logging
from evobandits.evobandits import (
    EvoBandits,
)
from evobandits.params import BaseParam

_logger = logging.get_logger(__name__)


ParamsType: TypeAlias = Mapping[str, BaseParam]


ALGORITHM_DEFAULT = EvoBandits()


class Study:
    """
    A Study represents an optimization task consisting of a set of trials.

    This class provides interfaces to optimize an objective function within specified bounds
    and to manage user-defined attributes related to the study.
    """

    def __init__(self, seed: int | None = None, algorithm=ALGORITHM_DEFAULT) -> None:
        """
        Initialize a Study instance.

        Args:
            seed: The seed for the Study. Defaults to None (use system entropy).
            algorithm: The optimization algorithm to use. Defaults to EvoBandits.
        """
        if seed is None:
            _logger.warning("No seed provided. Results will not be reproducible.")
        elif not isinstance(seed, int):
            raise TypeError(f"Seed must be integer: {seed}")

        self.seed: int | None = seed
        self.algorithm = algorithm  # ToDo Issue #23: type and input validation
        self.objective: Callable | None = None  # ToDo Issue #23: type and input validation
        self.params: ParamsType | None = None  # ToDo Issue #23: Input validation

    def _collect_bounds(self) -> list[tuple[int, int]]:
        """
        Collects the bounds of all parameters in the study.

        Returns:
            list[tuple[int, int]]: A list of tuples representing the bounds for each parameter.
        """
        bounds = []
        for param in self.params.values():
            bounds.extend(param.bounds)
        return bounds

    def _decode(self, action_vector: list) -> dict:
        """
        Decodes an action vector to a dictionary that contains the solution for each parameter.

        Args:
            action_vector (list): A list of actions to map.

        Returns:
            dict: The distinct solution for the action vector, formatted as dictionary.
        """
        result = {}
        idx = 0
        for key, param in self.params.items():
            result[key] = param.decode(action_vector[idx : idx + param.size])
            idx += param.size
        return result

    def _evaluate(self, action_vector: list) -> float:
        """
        Execute a trial with the given action vector.

        Args:
            action_vector (list): A list of actions to execute.

        Returns:
            float: The result of the objective function.
        """
        solution = self._decode(action_vector)
        return self.objective(**solution)

    def optimize(self, objective: Callable, params: ParamsType, trials: int) -> None:
        """
        Optimize the objective function.

        The optimization process involves selecting suitable hyperparameter values within
        specified bounds and running the objective function for a given number of trials.

        Args:
            func (Callable): The objective function to optimize.
            params (dict): A dictionary of parameters with their bounds.
            trials (int): The number of trials to run.

        Returns:
            dict: The best parameter values found during optimization.
        """
        self.objective = objective
        self.params = params

        bounds = self._collect_bounds()
        best_action_vector = self.algorithm.optimize(self._evaluate, bounds, trials, self.seed)

        return self._decode(best_action_vector)
