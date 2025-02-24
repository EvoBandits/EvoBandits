# Params Module

The `params` module provides a flexible and robust way to handle parameters for gmab.

## Motivation

On the one hand, we agree that having a "bulky" interface for defining and handling parameters
might not be an ideal solution.

On the other hand, a lot of freedom over how parameters can be defined (like in the example below)
will require more complex validation in the `Study` module. The validation, and especially the
mapping from gmab's internal action_vector to the solution is depends on how each individual
parameter has been defined by the user.

```python
from sklearn.utils.fixes import loguniform
{'C': loguniform(1e0, 1e3),
 'gamma': loguniform(1e-4, 1e-3),
 'kernel': ['rbf'],
 'class_weight':['balanced', None]}
```

Therefore, a streamlined interface to define and handle parameters for the Study module is
desirable, leading to the idea of this approach:

* As each parameter is defined separately by the user depending on their specific requirements,
pygmab should offer intefaces for each type of parameter.
* A "type" summarizes parameters have similar requirements, specifically: Similar steps to
define their bounds and map their values from gmab's internal action_vector. For now, there will
be the types: Integer, Float, and Categorical.
* Having a class for each type guarantess separation of concern and extensibility for how different
parameters can be converted to integer representation that the gmab algorithm will handle.
* At the same time, the types need to implement a "generic" interface that the Study is able to
access, possibly through inheritance.

Example usage:
```python
# Definition of parameters (User):
params = {
   "a": IntParam(low=0, high=1000, size=10, step=20)
   "b": FloatParam(low=0, high=1, step=100) # Future work
   "c": CategoricalParam(['balanced', 'None']) # Future work
}

# Collect the bounds for all parameters (Study module).
bounds = [p.bounds for p in params.values()]
```

## Implementation

### Class: `IntParam`

The `IntParam` class encapsulates an integer parameter with a defined range
(`low` to `high`) and step size. It supports mapping input values to this range.

## Example Usage

```python
# Create a new parameter
from gmab import IntParam
param = IntParam(low=1, high=10, size=3, step=2)

# Access the bounds
print(param.bounds)  # Output: [(1, 6), (1, 6), (1, 6)]

# Map a list of actions to values
values = param.map_to_value([0, 1, 2])
print(values)  # Output: [1, 3, 5]
```
