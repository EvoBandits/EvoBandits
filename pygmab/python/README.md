# Vision for pygmab interface
Suggestions how a user interface for pygmab can be implemented. Feel free to comment!

## 1. Create a Study

Use `initialize()` to initialize instances of `Study`, which is a class that handles algorithm
control, and `Bounds`, which is a class that handles the algorithm's bounds and mapping of all parameters.

```python
import gmab

study, bounds = gmab.initialize(seed=42) # prev. gmab.create_study()
```

## 2. Define objective and bounds

The direct interface with rust uses a list of integers as action_vector, where a tuple `(low, high)`
defines the bounds for each element of the action_vector. The action_vector is then used to
simulate the objective.

From [./examples/tester.py](https://github.com/E-MAB/GMAB/blob/add-pygmab-readme/examples/tester.py)

```python
from gmab import Gmab

def rosenbrock_function(number: list):
    return sum(
        [
            100 * (number[i + 1] - number[i] ** 2) ** 2 + (1 - number[i]) ** 2
            for i in range(len(number) - 1)
        ]
    )

if __name__ == "__main__":
    bounds = [(-5, 10), (-5, 10)]
    gmab = Gmab(rosenbrock_function, bounds)
    ...
```

While this works well for an objective function with one integer decision vector, users will
expect an interface that enables dynamically setting bounds for multiple parameters and types.

Internally, this will require:

* Handling and checking the user's inputs to create the `bounds` tuple that is expected by
rust-gmab when starting the optimization.
* For each simulation, mapping the action_vector generated in rust to the `kwargs` of the objective.
* For example, the value `1` in the action_vector will be mapped to `10` if the parameter is
configured with `bounds.suggest_int(low=0, high=100, steps=10)`.
* Alternatively, the value `1` in the action_vector will be mapped to `manhattan` if the
parameter is configured with `bounds.suggest_categorical(["euclidean", "manhattan", "canberra"])`.

Below are two examples to illustrate how users will be able to define the objective and the
params.

### Net present value example (just for illustration of the UI)

Similar to the integer decision vector of the rosenbrock function, the calculation of the net present
value requires a `cash_flows` vector.

In addition, an interest rate is also needed to calculate the NPV. With an `objective(numbers: list)`
type of function, the user would need to explicitly handle this in the objective function.

```python
def objective(cash_flows: list, interest: float) -> float:
    return sum([cf / (1 + interest) ** t for t, cf in enumerate(cash_flows)])

params = {
    "cash_flows": bounds.suggest_int(low=0, high=100000, step=100, size=3),
    "interest": bounds.suggest_float(low=0.0, high=0.1, step=0.001)
}
```

### Clustering Example

Compared to the rosenbrock function - and other integer decision problems - the tuning of
ML models requires a variety of inputs, like in the example below.

```python
from sklearn.cluster import DBSCAN
from sklearn.metrics import silhouette_score

# Assume data is defined as x_train

def objective(eps: float, min_samples:int, metric: str) -> float:
    clusterer = DBSCAN(eps=eps, min_samples=min_samples, metric=metric)
    clusterer.fit(x_train)
    return silhouette_score(x_train, clusterer.labels_)

params = {
    "eps": bounds.suggest_float(low=0.1, high=0.9, step=0.001),
    "min_samples": bounds.suggest_int(low=2, high=10),
    "metric": bounds.suggest_categorical(["euclidean", "manhattan", "canberra"]),
}
```

## 3. Optimization

Use `study.optimize()` to start optimization with given settings.

Names for settings are (somewhat) based on:

* [optuna.study.Study](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.study.Study.html#optuna.study.Study)
* [optuna.samplers.NSGAIISampler](https://optuna.readthedocs.io/en/stable/reference/samplers/generated/optuna.samplers.NSGAIISampler.html)


| Name              | Description                                                             |
|-------------------|-------------------------------------------------------------------------|
| `max_time`        | Maximum execution time per algorithm instance                           |
| `max_trials`      | Maximum number of simulations per algorithm instance                    |
| `population_size` | Number of individuals (trials) in a generation                          |
| `crossover_rate`  | Probability for a crossover (exchange of values between individuals)    |
| `mutation_rate`   | Probability for a mutation (change to a value of an individual)         |
| `mutation_span`   | Sets how much a value is altered during mutation                        |
| `...`             | Other parameters to set verbose, parallelization, name, ...             |


Internally, the method will store and transform the user inputs for rust-gmab, and then create
and execute the set number of algorithm instances. Finally, it will also collect the results.

```python
study.optimize(objective, params, n_trials=5, n_simulations=10000, popsize=100, ...)
```

## 4. Access the results (additional features TBD.)

Use `study.best_trial()` to output the best result that has been returned.

```python
result = study.best_trial()

```
