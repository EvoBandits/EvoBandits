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

## Design Aspects

### Class: `IntParam`

The `IntParam` class encapsulates an integer parameter with a defined range
(`low` to `high`) and step size. It supports mapping input values to this range.

### Function: `suggest_int`

The `suggest_int` function is a factory function that creates an instance of `IntParam` with
validated inputs. It ensures that the parameters are integers and that the bounds and step sizes
are logically consistent.

## Example Usage

```python
# Create a new set of parameters
from gmab import suggest_int
param = suggest_int(low=1, high=10, size=3, step=2)

# Access the bounds of the parameter
print(param.bounds)  # Output: [(1, 6), (1, 6), (1, 6)]

# Map a list of actions to the parameter
values = param.map_to_value([0, 1, 2])
print(values)  # Output: [1, 3, 5]
