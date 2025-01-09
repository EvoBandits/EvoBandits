from pygmab import call_python_function_with_chosen_arg

def test_function(number):
    return number ** 2

if __name__ == '__main__':
    print(call_python_function_with_chosen_arg(test_function))
