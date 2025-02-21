# Params Module

The `params` module provides a flexible and robust way to handle parameters for gmab.

## Vocabulary

- **Value**: Corresponds to an actual value of a parameter of the user's objective function.
The value is valid within the specified constraints (type, limits, size) of the parameter.
- **Solution**: A set of values that can be used as (valid) input for the objective function.
- **Action**: The internal, integer representation of a parameter's value that gmab uses for
optimization. An action always corresponds to one distint value for a parameter.
- **Bounds**: The internal, integer representation of a parameter's constraints (limits, size) that
is used by gmab. The bounds constrain the selection (=sampling, mutation) of actions.
- **Action Vector**: A set of actions that serve as internal representation of one distinct solution.
- **Mapping**: Translation of an action (action_vector) to it's value (solution), or reversed.

## Implementation

### Class: `IntParam`

The `IntParam` class encapsulates an integer parameter with a defined range
(`low` to `high`) and step size. It supports mapping input values to this range.

### Function: `suggest_int`

The `suggest_int` function is a factory function that creates an instance of `IntParam` with
validated inputs. It ensures that the parameters are integers and that the bounds and step sizes
are logically consistent.

## Example Usage

```python
# Create a new parameter
from gmab import suggest_int
param = suggest_int(low=1, high=10, size=3, step=2)

# Access the bounds of the parameter
print(param.bounds)  # Output: [(1, 6), (1, 6), (1, 6)]

# Map a list of actions to the parameter
values = param.map_to_value([0, 1, 2])
print(values)  # Output: [1, 3, 5]
```

## Potential Advantages of this Design:

We aggree that having a separate class for defining and holding parameters, instead of just exposing `suggest_int` is not ideal. Example:

```python
import gmab

study, config = gmab.initialize()

bounds = {
   "dim_1": config.suggest_int(0, 10, size=2),
   "dim_2": config.suggest_int(0, 10, size=2)
}
```

On the other hand, having a lot of freedom over the values of the params
dictionary is not needed for the user: The gmab algorithm can handle only discrete
parameter (list of numbers or categoricals). Besides, more freedom for the user means more complicated validation and handling them in code, and more potential of errors when defining the params. Example:

```python
from sklearn.utils.fixes import loguniform
{'C': loguniform(1e0, 1e3),
 'gamma': loguniform(1e-4, 1e-3),
 'kernel': ['rbf'],
 'class_weight':['balanced', None]}
```

The approach above tries to combine both aspects by having an instance of a class
`Param` for each parameter. This can provide both a streamlined interface for
defining the parameter, as well as enough standardization so that `Study`
can easily handle the inputs in a unified way:

- Each Parameter needs to offer an interface for creating bounds (`(low, high)` tuples of a specified `size`) and mapping actions to values.
- Depending on the Parameter type, additional functionality may be required, for
example for handling lookup of categories

Currently, only an IntParam is implemented. In the future, other types of parameteres
can be added without changes to Study, if they are inherited, for example like:

```plaintext
ABCParam
├── size
├── low
├── high
├── bounds
└── map_to_value
|
├── IntParam
│   ├── step
│   ├── bounds
│   └── map_to_value
|
└── CategoricalParam
    ├── lookup_table
    └── map_to_value
