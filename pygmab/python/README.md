# Vision for pygmab interface
Suggestions how a user interface for pygmab can be implemented. Feel free to comment!

## 1. Create a Study

Use create_study() to initialize an instance of Study, which is a class that handles algorithm
control, and Bounds, which is a class that handles the algorithm's bounds and mapping of all parameters.

```python
import gmab

study, bounds = gmab.create_study(seed=42)
```

## 2. Define objective and bounds

Rust-gmab uses a list of integers as action_vector, where a tuple (low. high) defines the bounds
for each element of the action_vector. The action_vector is then used as single parameter to simulate
with the objective function.

From examples/tester.py:

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

While this works well for an objective function with one integer decision vector, users likely
expect a simple, and more interactive interface that enables setting bounds for multiple parameters,
and with different types.

Internally, this will require:

* Handling and checking the user's inputs to create the bounds tuple for rust-gmab before
starting the optimization.
* For each simulation, mapping the action_vector from rust to the kwargs of the objective.
* For example, the value `1` in the action_vector will be mapped to `10` if the parameter is
configured with bounds.suggest_int(low=0, high=100, steps=10).
* Alternatively, the value `1` in the action_vector will be mapped to `manhattan` if the
parameter is configured with bounds.suggest_categorical(["euclidean", "manhattan", "canberra"])

Below are two examples to illustrate how users will be able to define the objective and the
params.

### Net present value example (just for illustration of UI)

Compared to the rosenbrock function, a similar vector (list of numbers) is input as cash_flows
if the net present value is calculated. The implementation below would enable the user to
dynamically set bounds for cash_flows (in example: 3 periods, with 100 values between 0 and 100_000)

In addition, an interest rate is also needed as input, which would be complicated to manage
with an `objective(numbers: list)` type of function due to the different variable type and bounds.

```python
def objective(cash_flows: list, interest: float) -> float:
    return sum([cf / (1 + interest) ** t for t, cf in enumerate(cash_flows)])

params = {
    "cash_flows": bounds.suggest_int(low=0, high=100000, steps=100, size=3),
    "interest": bounds.suggest_float(low=0.0, high=0.1, steps=100)
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
    clusterer = DBSCAN(eps, min_samples, metric)
    clusterer.fix(x_train)
    return silhouette_score(x_train, clusterer.labels_)

params = {
    "eps": bounds.suggest_float(low=0.1, high=0.9, steps=10),
    "min_samples": bounds.suggest_int(low=2, high=10),
    "metric": bounds.suggest_categorical(["euclidean", "manhattan", "canberra"]),
}
```

## 3. Optimization

Use `study.optimize()` to start optimization with given settings.

Internally, the method will need to store and transform the user inputs for rust-gmab,
and then create and execute the set number of algorithm instances. Finally, it will also
collect the results in a storage.

```python
study.optimize(objective, params, n_trials=5, n_simulations=10000, popsize=100, ...)
```

## 4. Access the results (TBD.)

Use `study.best_trial()` to output the best result that has been returned.

```python
result = study.best_trial()

```
