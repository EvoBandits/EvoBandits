from pygmab import optimizer as gmab

def test_function(number: list):
    return sum([i ** 2 for i in number])

def rosenbrock_function(number: list):
    return sum([100 * (number[i + 1] - number[i] ** 2) ** 2 + (1 - number[i]) ** 2 for i in range(len(number) - 1)])

if __name__ == '__main__':
    bounds = [(-5, 10), (-5, 10)]
    print(gmab(rosenbrock_function, bounds, 10000))
