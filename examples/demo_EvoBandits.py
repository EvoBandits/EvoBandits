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

from evobandits import EvoBandits


def rosenbrock_function(number: list):
    return sum(
        [
            100 * (number[i + 1] - number[i] ** 2) ** 2 + (1 - number[i]) ** 2
            for i in range(len(number) - 1)
        ]
    )


if __name__ == "__main__":
    bounds = [(-5, 10), (-5, 10)]
    n_trials = 10000
    n_best = 3
    evobandits = EvoBandits()
    best_arms = evobandits.optimize(rosenbrock_function, bounds, n_trials, n_best)

    print("Number of Results:", len(best_arms))  # matches n_best

    # print action_vector, value, variance, std_dev and n_evaluations for best arm
    # variance and std_dev should be 0.0, as objective function is deterministic
    print(best_arms[0].to_dict)
