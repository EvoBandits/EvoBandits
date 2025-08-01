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
from collections.abc import Callable, Mapping
from inspect import signature
from random import Random
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

        # 1 for minimization, -1 for maximization to avoid repeated branching during optimization.
        self._direction: int = 1
        self._params: ParamsType
        self._objective: Callable
        self._results: list[dict[str, Any]]
        self._seeded_call = None
        self._rng = None

    @staticmethod
    def _ucb_ranking(results: list[dict[str, Any]], direction: int) -> list[dict[str, Any]]:
        """
        Ranks results using the Upper Confidence Bound (UCB).

        The UCB is calculated as a sum of a normalized value and an exploration penalty:
        UCB = normalized_value + sqrt(2 * ln(total_evaluations) / n_evaluations)

        Args:
            results: A list of dictionaries, each containing
                'value' (float): The observed value (e.g., mean reward or cost) of the arm, and
                'n_evaluations' (int): The number of times the arm has been evaluated.
            direction: 1 for minimization, -1 for maximization of the Study's objective

        Returns:
            The results with each dictionary updated with a new key
                'ucb_rank' (int): The ranking position of the arm based on the computed UCB value.
        """
        total_evaluations = sum(r["n_evaluations"] for r in results)
        ucb_norm_min = min(r["value"] for r in results)
        ucb_norm_max = max(r["value"] for r in results)

        if ucb_norm_min != ucb_norm_max:
            denom = ucb_norm_max - ucb_norm_min
        else:
            denom = 1e-9  # prevent div by zero

        # Compute UCB value
        for r in results:
            normalized_value = (r["value"] - ucb_norm_min) / denom
            penalty = math.sqrt(2.0 * math.log(total_evaluations) / r["n_evaluations"])
            r["ucb_rank"] = normalized_value + penalty * direction

        # Convert UCB value -> ranking
        sorted_results = sorted(results, key=lambda x: direction * x["ucb_rank"])
        for rank, r in enumerate(sorted_results, start=1):
            r["ucb_rank"] = rank

        return sorted_results

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

    def _generate_seed(self) -> int:
        """Returns a random seed for objective evaluations."""
        return self.rng.randint(0, 2**32 - 1)

    def _evaluate(self, action_vector: list[int]) -> float:
        """
        Execute a trial with the given action vector.

        Args:
            action_vector: The encoded representation of parameter values.

        Returns:
            The value from a single evaluation of the objective function.
        """
        solution = self._decode(action_vector)

        if self.seeded_call:
            solution.update({"seed": self._generate_seed()})

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
        if "seed" in params.keys():
            raise ValueError(
                "A parameter named 'seed' was found in the decision space at `study.params`. "
                "Using 'seed' as a parameter can cause conflicts with the internal RNG used by "
                "the Study. Please consider renaming this parameter to avoid ambiguity."
            )
        self._params = params

        # input validation for objective, n_trials, n_best is managed by 'self.algorithm'
        self._objective = objective
        bounds = self._collect_bounds()
        results = []

        for _ in range(n_runs):
            seed = self._generate_seed()  # new entropy for each seeded run
            algorithm = self.algorithm.clone()
            best_arms = algorithm.optimize(self._evaluate, bounds, n_trials, n_best, seed)

            for arm in best_arms:
                result = arm.to_dict
                action_vector = result.pop("action_vector")
                result["params"] = self._decode(action_vector)
                results.append(result)

        # Save results and apply UCB ranking
        self.results = results

    @property
    def seeded_call(self) -> bool:
        """
        Indicates whether a seed is passed to the objective function during evaluation.

        Returns:
            True if `self.seed` is set and the `_objective` function accepts a 'seed';
            False otherwise.
        """
        if self._seeded_call is None:
            self._seeded_call = (
                self.seed is not None and "seed" in signature(self._objective).parameters
            )
        return self._seeded_call

    @property
    def rng(self) -> Random:
        """
        The Study's generator (RNG) instance.

        If a seed was provided at initialization, the RNG is seeded with it for reproducibility.
        Otherwise, a new RNG instance using system entropy is created.

        Returns:
            The RNG instance used for generating random numbers.
        """
        if not self._rng:
            self._rng = Random(self.seed) if self.seed else Random()
        return self._rng

    @property
    def results(self) -> list[dict[str, Any]]:
        """
        Ranks and returns all results found during optimization.

        Returns:
            A list of ranked results (as dictionaries) found during optimization.
        """
        if not self._results:
            raise AttributeError("Study has no results. Run study.optimize() first.")
        return self._ucb_ranking(self._results, self._direction)

    @results.setter
    def results(self, results: list[dict[str, Any]]) -> None:
        """
        Sets the Study's raw results.

        Args:
            A list of results (as dictionaries) found during optimization.
        """
        self._results = results

    @property
    def best_value(self) -> float:
        """
        Returns the best value found during optimization.

        Returns:
            The best value among `study.results`.
        """
        return next(r["value"] for r in self.results if r["ucb_rank"] == 1)

    @property
    def mean_value(self) -> float:
        """
        Returns the mean value of all results found during optimization.

        Returns:
            The mean value of `study.results`.
        """
        return mean([r["value"] for r in self.results])

    @property
    def best_solution(self) -> dict[str, Any]:
        """
        Returns the best solution found during optimization.

        Returns:
            The solution (as a dictionary) that yielded `study.best_value`.
        """
        return next(r for r in self.results if r["ucb_rank"] == 1)

    @property
    def best_params(self) -> dict[str, Any]:
        """
        Returns the parameter set corresponding to the best value found during optimization.

        Returns:
            The parameters (as a dictionary) that yielded `study.best_value`.
        """
        return next(r["params"] for r in self.results if r["ucb_rank"] == 1)
