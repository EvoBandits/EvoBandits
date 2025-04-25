"""
Objective function and useful parameters for the multidimensional rosenbrock function
"""

from gmab import IntParam

PARAMS_2D = {"number": IntParam(-5, 10, 2)}

BOUNDS_2D = [(-5, 10), (-5, 10)]
RESULTS_2D = [1, 1]


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
