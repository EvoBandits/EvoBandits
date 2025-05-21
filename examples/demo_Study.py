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
from evobandits import Study, IntParam, EvoBandits


def noisy_rosenbrock(number: list):
    # Rosenbrock Function
    value = sum(
        [
            100 * (number[i + 1] - number[i] ** 2) ** 2 + (1 - number[i]) ** 2
            for i in range(len(number) - 1)
        ]
    )
    # Add Gaussian Noise
    value += random.normal(0, 5)
    return value


if __name__ == "__main__":
    # Define solution space for the objective
    params = {"number": IntParam(-5, 10, 2)}

    # Customize the algorithm configuration if needed
    my_evobandits = EvoBandits(population_size=100)

    # Execute the Optimization
    study = Study(seed=42, algorithm=my_evobandits)
    results = study.optimize(noisy_rosenbrock, params, 10000, n_best=3)

    print("Number of Results:", len(results))  # matches n_best
    [
        print(r) for r in results
    ]  # params, value, variance, std_dev, n_evaluations and position for each result
