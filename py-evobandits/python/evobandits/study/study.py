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

from collections.abc import Callable, Mapping
from statistics import mean
from typing import Any, TypeAlias

from evobandits import logging
from evobandits.evobandits import GMAB
from evobandits.params import BaseParam

_logger = logging.get_logger(__name__)


ParamsType: TypeAlias = Mapping[str, BaseParam]


ALGORITHM_DEFAULT = GMAB()


class Study:
    """
    A Study represents an optimization task.

    This class provides interfaces to optimize an objective function within specified bounds
    and to manage user-defined attributes related to the study.
    """

    def __init__(self, seed: int | None = None, algorithm: GMAB = ALGORITHM_DEFAULT) -> None:
        """
        Initializes a Study instance.

        Args:
            seed: The seed for the Study. Defaults to None (uses system entropy).
            algorithm: The optimization algorithm to use. Defaults to GMAB.
        """
        if seed is None:
            _logger.warning("No seed provided. Results will not be reproducible.")
        elif not isinstance(seed, int):
            raise TypeError(f"Seed must be integer: {seed}")

        self.seed: int | None = seed
        self.algorithm: GMAB = algorithm
        self.results: list[dict[str, Any]] = []

        # 1 for minimization, -1 for maximization to avoid repeated branching during optimization.
        self._direction: int = 1
        self._params: ParamsType
        self._objective: Callable

    def _collect_bounds(self) -> list[tuple[int, int]]:
        """
        Collects the bounds of the parameter configuration saved to `self._params`.

        Returns:
            The bounds, a list of (lower_bound, upper_bound) tuples for all parameters.
        """
        bounds = []
        for param in self._params.values():
            bounds.extend(param.bounds)
        return bounds

    def _decode(self, action_vector: list[int]) -> dict[str, Any]:
        """
        Decodes an action vector into a dictionary mapping parameter names to their decoded values.

        Args:
            action_vector: The encoded representation of parameter values.

        Returns:
            A dictionary of parameter names and their decoded values.
        """
        result = {}
        idx = 0
        for key, param in self._params.items():
            result[key] = param.decode(action_vector[idx : idx + param.size])
            idx += param.size
        return result

    def _evaluate(self, action_vector: list[int]) -> float:
        """
        Execute a trial with the given action vector.

        Args:
            action_vector: The encoded representation of parameter values.

        Returns:
            The value from a single evaluation of the objective function.
        """
        solution = self._decode(action_vector)
        evaluation = self._direction * self._objective(**solution)
        return evaluation

    def optimize(
        self,
        objective: Callable,
        params: ParamsType,
        n_trials: int,
        maximize: bool = False,
        n_best: int = 1,
        n_runs: int = 1,
    ) -> None:
        """
        Optimize the objective function, saving results to `study.results`.

        The optimization process involves selecting suitable hyperparameter values within
        specified bounds and running the objective function for a given number of trials.

        Args:
            objective: The objective function to optimize.
            params: A dictionary of parameters with their bounds.
            n_trials: The number of evaluations to perform on the objective.
            maximize: Indicates if objective is maximized. Default is False.
            n_best: The number of results to return per run. Default is 1.
            n_runs: The number of times optimization is repeated. Default is 1.
        """
        if not isinstance(maximize, bool):
            raise TypeError(f"maximize must be a bool, got {type(maximize)}.")
        self._direction = -1 if maximize else 1

        if not isinstance(n_runs, int):
            raise TypeError(f"n_runs must be an int larger than 0, got {type(n_runs)}.")
        if n_runs < 1:
            raise ValueError(f"n_runs must be an int larger than 0, got {n_runs}.")

        if not isinstance(params, Mapping):
            raise TypeError(f"params must be a mapping, got {type(params)}.")
        for k, v in params.items():
            if not isinstance(k, str):
                raise TypeError(f"Parameter key must be str, got {type(k)}.")
            if not isinstance(v, BaseParam):
                raise TypeError(f"Parameter '{k}' must implement BaseParam, got {type(v)}.")
        self._params = params

        # input validation for objective, n_trials, n_best is managed by 'self.algorithm'
        self._objective = objective

        bounds = self._collect_bounds()

        for run_id in range(n_runs):
            seed = self.seed + run_id if self.seed else None  # new entropy for each seeded run
            algorithm = self.algorithm.clone()
            best_arms = algorithm.optimize(self._evaluate, bounds, n_trials, n_best, seed)

            for n_best, arm in enumerate(best_arms, start=1):
                result = arm.to_dict
                action_vector = result.pop("action_vector")
                result["params"] = self._decode(action_vector)
                result["n_best"] = n_best
                result["run_id"] = run_id
                self.results.append(result)

    @property
    def best_value(self) -> float:
        """
        Returns the best value found during optimization.

        Returns:
            The best value among `study.results`.
        """
        if not self.results:
            raise AttributeError("Study has no results. Run study.optimize() first.")
        return max(self.results, key=lambda r: -self._direction * r["value"])["value"]

    @property
    def mean_value(self) -> float:
        """
        Returns the mean value of all results found during optimization.

        Returns:
            The mean value of `study.results`.
        """
        if not self.results:
            raise AttributeError("Study has no results. Run study.optimize() first.")
        return mean([r["value"] for r in self.results])

    @property
    def best_solution(self) -> dict[str, Any]:
        """
        Returns the best solution found during optimization.

        Returns:
            The solution (as a dictionary) that yielded `study.best_value`.
        """
        if not self.results:
            raise AttributeError("Study has no results. Run study.optimize() first.")
        return next(r for r in self.results if r["value"] == self.best_value)

    @property
    def best_params(self) -> dict[str, Any]:
        """
        Returns the parameter set corresponding to the best value found during optimization.

        Returns:
            The parameters (as a dictionary) that yielded `study.best_value`.
        """
        return self.best_solution["params"]
