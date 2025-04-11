def rb_function(number: list):
    """Computes the value of the multidimensional rosenbrock function."""
    return sum(
        [
            100 * (number[i + 1] - number[i] ** 2) ** 2 + (1 - number[i]) ** 2
            for i in range(len(number) - 1)
        ]
    )
