# Vision for py-evobandits interface
Suggestions how a user interface for py-evobanits can be implemented. Feel free to comment!

## 1. Define objective and bounds

The direct interface with rust uses a list of integers as action_vector, where a tuple `(low, high)`
defines the bounds for each element of the action_vector. The action_vector is then used to
simulate the objective.

From [./examples/tester.py](https://github.com/EvoBandits/EvoBandits/blob/add-py-bandits-readme/examples/tester.py)

```python
from evobandits import EvoBandits

def rosenbrock_function(number: list):
    return sum(
        [
            100 * (number[i + 1] - number[i] ** 2) ** 2 + (1 - number[i]) ** 2
            for i in range(len(number) - 1)
        ]
    )

if __name__ == "__main__":
    bounds = [(-5, 10), (-5, 10)]
    evobandits = EvoBandits(rosenbrock_function, bounds)
    ...
```

To simplify the modeling of complex decision problems, with different types of parameters, a
python interface is provided that verifies the user's input, creates bounds for the optimization,
and handles the discretisation of floata parameters and label encoding of categorical parameters among other things.

Below are two examples to illustrate how users will be able to define the objective and the
params.

### Net present value example (just for illustration of the UI)

Similar to the integer decision vector of the rosenbrock function, the calculation of the net present
value requires a `cash_flows` vector.

In addition, an interest rate is also needed to calculate the NPV. With an `objective(numbers: list)`
type of function, the user would need to explicitly handle this in the objective function.

```python
from evobandits import IntParam, FloatParam

def objective(cash_flows: list, interest: float) -> float:
    return sum([cf / (1 + interest) ** t for t, cf in enumerate(cash_flows)])

params = {
    "cash_flows": IntParam(low=0, high=100000, step=100, size=3),
    "interest": FloatParam(low=0.0, high=0.1, step=0.001)
}
```

### Clustering Example

Compared to the rosenbrock function - and other integer decision problems - the tuning of
ML models requires a variety of inputs, like in the example below.

```python
from sklearn.cluster import DBSCAN
from sklearn.metrics import silhouette_score

from evobandits import IntParam, FloatParam, CategoricalParam

# Assume data is defined as x_train

def objective(eps: float, min_samples:int, metric: str) -> float:
    clusterer = DBSCAN(eps=eps, min_samples=min_samples, metric=metric)
    clusterer.fit(x_train)
    return silhouette_score(x_train, clusterer.labels_)

params = {
    "eps": suggest_float(low=0.1, high=0.9, step=0.001),
    "min_samples": IntParam(low=2, high=10),
    "metric": CategoricalParam(["euclidean", "manhattan", "canberra"]),
}
```

## 2. Create a Study

The Study class handles optimization and provides an interface to store parameters and results.

```python
from evobandits import Study

study = evobandits.Study(seed=42)
```

## 3. Optimization

Use `study.optimize()` to start optimization with given settings.

Internally, the method will store and transform the user inputs for rust-evobandits, and then create
and execute the set number of algorithm instances. Finally, it will also collect the results.

```python
study.optimize(objective, params, trials=10000, population_size=100, ...)
```

## 4. Access the results (TBD.)

Use `study.best_trial()` to output the best result that has been returned.

```python
result = study.best_trial()

```
