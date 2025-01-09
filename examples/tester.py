from pygmab import optimizer as gmab

def test_function(number: list):
    return sum([i ** 2 for i in number])

if __name__ == '__main__':
    bounds = [[-10, 10], [-10, 10]]
    print(gmab(test_function, bounds))
