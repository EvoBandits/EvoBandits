## Summary
The simulation of the objective function is often the most demanding part of an experiment, especially when simulating with an efficient optimizer. This guide demonstrates how to accelerate simulation with EvoBandits using [`Numba`](https://numba.pydata.org/), an open source JIT compiler, using a simple example.

## Efficient Objective Function
The example optimizes the configuration of a simple test function, which is referred to as Test Problem 4 (TP4) and explained in detail in the [GMAB Paper](https://ieeexplore.ieee.org/document/10818791) by Preil & Krapp (2025). With regard to the numba acceleration, it can be seen as a lightweight example representing more complex objectives that might leverage full Numba capabilities such as parallelization or GPU acceleration.

```python
from numba import njit
import numpy as np

@njit
def tp4_func(action_vector: np.ndarray, seed: int = -1) -> float:
    ... # simulation logic
    return res
```

## Reproducibility of Results
Since numba-compiled functions cannot use a global RNG seed at this time, the optimizer must generate and pass a new seed for each evaluation of the objective if results shall be reproduced:

* As shown above, `tp4_func` must accept a parameter `seed`. In this instance, a sentinel value of `-1` is used instead of `None` to denote an unseeded run, as this avoids a more complex and explicit numba setup that handles an optional function argument.
* A seed must be passed to the `Study` on initialization to set up a seeded experiment. The Study will then automatically generate an independent seed from the range of non-negative integers for each evaluation and pass it to `tp4_func`.

## Simulation
EvoBandits treats Numba-compiled and pure Python functions equivalently. For details on the configuration and execution of the optimization, please refer to the Reference and other examples on this page.

```python
if __name__ == "__main__":
    # Model a five-dimensional instance of TP4.
    params = {"action_vector": IntParam(-100, 100, 5)}
    n_trials = 20_000
    n_runs = 10

    # Execute optimization
    study = Study(seed=42)
    study.optimize(tp4_func, params, n_trials, n_runs=n_runs)
    print("Best solution found during optimization: ", study.best_value)
    print("Mean result:", study.mean_value)
    print("Best configuration: ", study.best_params)
```

Example Output:
```
Best solution found during optimization:  -2548.569595505386
Mean result: -2449.193337282534
Best configuration:  {'action_vector': [54, 55, 57, 57, 57]}
```

## References

```
Preil, D., & Krapp, M. (2024). Genetic Multi-Armed Bandits: A Reinforcement Learning Inspired Approach for Simulation Optimization. IEEE Transactions on Evolutionary Computation.
```

## Try it yourself!
The complete example is available on [Github](https://github.com/EvoBandits/EvoBandits/blob/main/examples/efficient_objective_function.py). Running it requires additional dependencies, which can be installed using:

```bash
pip install evobandits[examples]
```

This command will install Numba and other packages required to run example scripts.
