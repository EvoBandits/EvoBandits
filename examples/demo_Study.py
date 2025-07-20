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

from numpy import random
from evobandits import Study, IntParam, GMAB


def noisy_rosenbrock(number: list, seed: int | None = None):
    # Rosenbrock Function
    value = sum(
        [
            100 * (number[i + 1] - number[i] ** 2) ** 2 + (1 - number[i]) ** 2
            for i in range(len(number) - 1)
        ]
    )
    # Add Gaussian Noise
    rng = random.default_rng(seed)
    value += rng.normal(0, 5)
    return value


if __name__ == "__main__":
    # Define solution space for the objective
    params = {"number": IntParam(-5, 10, 2)}

    # Customize the algorithm configuration if needed
    my_algorithm = GMAB(population_size=100)

    # Execute the Optimization
    study = Study(seed=42, algorithm=my_algorithm)
    study.optimize(noisy_rosenbrock, params, 20000, n_best=1, n_runs=10)

    print("Number of Results:", len(study.results))  # matches n_best * n_runs
    print("Best configuration:", study.best_params)
    print("Best result: ", study.best_value)
    print("Mean result:", study.mean_value)
