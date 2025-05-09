from evobandits import Study, IntParam, EvoBandits


def rosenbrock_function(number: list):
    return sum(
        [
            100 * (number[i + 1] - number[i] ** 2) ** 2 + (1 - number[i]) ** 2
            for i in range(len(number) - 1)
        ]
    )


if __name__ == "__main__":
    # Define solution space for the objective
    params = {"number": IntParam(-5, 10, 2)}

    # Customize the algorithm configuration if needed
    my_evobandits = EvoBandits(population_size=100)

    # Execute the Optimization
    study = Study(seed=42, algorithm=my_evobandits)
    best_trial = study.optimize(rosenbrock_function, params, 100)
    print(best_trial)
