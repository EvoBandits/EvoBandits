## Random seeding with EvoBandits

Reproducibility in EvoBandits depends on the user’s control over randomness inside the objective function. While the optimization process itself can be seeded, deterministic or reproducible behavior of the objective must also be ensured manually. This can be achieved in different ways:

=== "seeding per evaluation (preferred)"

    Here, seeding is fully controlled by EvoBandits. If initialized with a random seed, `Study` automatically generates an independent, non-negative seed for each evaluation and propagates it to the objective function.

    ```python
    from evobandits import Study

    def noisy_rosenbrock(number: list, seed: int | None = None):
        ... # simulation logic
        return value

    study = Study(seed=42)
    ```

=== "global seeding"

    A random seed can be applied globally to control the objective function. However, a seed must still be passed to `Study` to control the optimization process itself, including sampling and algorithm behavior.

    ```python
    import random
    from evobandits import Study

    SEED = 42
    random.seed(SEED)

    def noisy_rosenbrock(number: list):
        ... # simulation logic
        return value

    study = Study(seed=SEED)
    ```

=== "unseeded (default)"

    By default, no seeding is applied and results are not reproducible.

    ```python
    from evobandits import Study

    def noisy_rosenbrock(number: list):
        ... # simulation logic
        return value

    study = Study()
    ```

!!! warning "Important: Seeding alone does not guarantee reproducibility. It relies on several factors:"

    - **Consistent configuration**: Even minor changes to the configuration can alter sampling behavior, despite identical seeds. The parameter definitions passed to evobandits (including types, ranges, and value ordering) must remain exactly the same across runs. Similarly, the optimizer setup must also be consistent to avoid hidden sources of variation (e.g. algorithm, budget, number of runs).

    - **Deterministic objective logic**: Your simulation or evaluation code should avoid non-deterministic behavior, such as parallelism, variable I/O timing, or reliance on external systems that may behave inconsistently between runs.

    - **Fully controlled randomness**: All sources of randomness used within your objective or preprocessing logic (e.g., `random`, `numpy.random`, or custom RNGs) must be explicitly seeded to ensure consistent behavior.

    - **Stable environment**: Reproducibility may also depend on your software and hardware environment, including Python version, library versions, operating system, and hardware architecture.

---

## Try it yourself!
You can experiment with seeding yourself using this simple example from the `evobandits.examples` module, available on [GitHub](https://github.com/EvoBandits/EvoBandits/blob/main/examples/demo_Study.py).

!!! note

    Running the examples requires additional dependencies, such as NumPy, which can be installed using:

    ```bash
    pip install evobandits[examples]
    ```

??? quote "Expand to copy `examples/efficient\_objective\_function.py`"

    ```python
    --8<-- "examples/efficient_objective_function.py"
    ```
