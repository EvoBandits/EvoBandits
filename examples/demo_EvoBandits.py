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
    evaluation_budget = 10000
    evobandits = EvoBandits()
    result = evobandits.optimize(rosenbrock_function, bounds, evaluation_budget)
    print(result)
