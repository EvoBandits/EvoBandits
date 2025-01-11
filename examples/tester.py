from gmab import Gmab

def test_function(number: list) -> float:
    return sum([i ** 2 for i in number])

def rosenbrock_function(number: list):
    return sum([100 * (number[i + 1] - number[i] ** 2) ** 2 + (1 - number[i]) ** 2 for i in range(len(number) - 1)])

if __name__ == '__main__':
    bounds = [(-5, 10), (-5, 10)]
    gmab = Gmab(rosenbrock_function, bounds)
    evaluation_budget = 10000
    result = gmab.optimize(evaluation_budget)
    print(result)
