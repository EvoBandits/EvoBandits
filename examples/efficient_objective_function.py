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


import numpy as np
from evobandits import IntParam, Study
from numba import njit

# Constants
BETA_1 = 300
BETA_2 = 500
GAMMA_1 = 0.001
GAMMA_2 = 0.005
EPS_1 = -38
EPS_2 = 56


@njit
def tp4_func(action_vector: np.ndarray, seed: int = -1) -> float:
    """
    Compute the function value for Test Problem 4 (TP4) from Preil & Krapp, 2025.

    Args:
        action_vector: A list of integers to calculate the TP4 function value with.
        seed: Optional random seed for reproducibility. Must be a positive integer.
            Defaults to -1, which acts as a sentinel value indicating no seeding.
            Note: -1 is used because Numba does not support None as a default argument.

    Source:
        D. Preil and M. Krapp, "Genetic Multi-Armed Bandits: A Reinforcement Learning Inspired
        Approach for Simulation Optimization," in IEEE Transactions on Evolutionary Computation,
        vol. 29, no. 2, pp. 360-374, April 2025, doi: 10.1109/TEVC.2024.3524505.
    """
    res = 0.0
    n = len(action_vector)
    for i in range(n):
        val = action_vector[i]
        res += BETA_1 * np.exp(-GAMMA_1 * (val - EPS_1) ** 2) + BETA_2 * np.exp(
            -GAMMA_2 * (val - EPS_2) ** 2
        )

    # Simulate Gaussian noise with std = 100 * len(action_vector)
    if seed != -1:
        np.random.seed(seed)
    res += np.random.normal(0.0, 100.0 * n)

    # Negate result to model a minimization problem
    res = -res

    return res


if __name__ == "__main__":
    # Model a five-dimensional instance of TP4.
    params = {"action_vector": IntParam(-100, 100, 5)}
    n_trials = 20_000
    n_runs = 10

    # Execute optimization
    study = Study(seed=42)
    study.optimize(tp4_func, params, n_trials, n_runs=n_runs)
    print("Best solution found during optimization: ", study.best_value)
    print("Mean result:", study.mean_value)
    print("Best configuration: ", study.best_params)
