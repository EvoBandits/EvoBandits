from pygmab import call_python_function_with_chosen_arg

def test_function(number: list):
    # list items ** 2 and then sum
    return sum([i ** 2 for i in number])

if __name__ == '__main__':
    print(call_python_function_with_chosen_arg(test_function))
