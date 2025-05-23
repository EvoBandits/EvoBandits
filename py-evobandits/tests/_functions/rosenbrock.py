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

"""
Objective function and useful parameters for the multidimensional rosenbrock function
"""

from evobandits import Arm, IntParam

# Bounds and best Arm to mock EvoBandits optimization (two-dimensional, for n_best = 1)
BOUNDS = [(-5, 10), (-5, 10)]
ARM_BEST = [Arm([1, 1])]

# Params and expected result to mock a Study (two-dimensional, with n_best = 1)
PARAMS = {"number": IntParam(-5, 10, 2)}
TRIAL_BEST = [{"n_best": 1, "value": 0.0, "n_evaluations": 0, "params": {"number": [1, 1]}}]


def function(number: list):
    return sum(
        [
            100 * (number[i + 1] - number[i] ** 2) ** 2 + (1 - number[i]) ** 2
            for i in range(len(number) - 1)
        ]
    )


if __name__ == "__main__":
    # Example usage
    result = function([1, 1])
    print(f"Value of the rosenbrock function: {result}")
