from gmab import Gmab, tester
import random

def rosenbrock_function(number: list):
    return sum([100 * (number[i + 1] - number[i] ** 2) ** 2 + (1 - number[i]) ** 2 for i in range(len(number) - 1)])

def random_noise_rosenbrock_function(number: list):
    return rosenbrock_function(number) + 0.1 * (2 * random.random() - 1)


if __name__ == '__main__':
    evaluation_budget = 10000
    bounds = [(-5, 10), (-5, 10)]
    gmab = Gmab(random_noise_rosenbrock_function, bounds)

    gmab.optimize(evaluation_budget)

    print(gmab.optimize(evaluation_budget))

    tester()
