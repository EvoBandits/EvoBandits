# 📘 Glossary

This glossary provides definitions of key terms related to the EvoBandits repository.
It is intended as a quick reference for contributors and users.

---

## Terms

#### Action vector

A discrete, integer decision vector that represents a distinct solution of the optimization problem. For integer decision problems with one decision parameter, the action vector is identical to the respective solution vector. For other problems that are modeled with the Python API, the action vector contains the value representations for all decision parameters. It can be transformed into the solution with encoding/decoding.

#### Bounds

A list of tuples that define the lower and upper bounds for each value of the action vector, and therefore, constrain the solution space for the optimization with EvoBandits. For problems that are modeled using the Python API, the bounds are derived from the specifications for the individual decision parameters that build the action vector.

#### Encoding / Decoding

If the user defines a solution space using the Python API, an encoding step is necessary to convert the solution to an action vector that is usable for optimization with EvoBandits. This step is trivial for integer parameters; however, a discretization step for float parameters and label encoding for categorical parameters is required.

#### EvoBandits Algorithm Options

The user can modify the conditions for the optimization using the following keywords:
- `population_size`: The number of starting solutions, and the number of individual solutions in a generation.
- `mutation_rate`: The probability that a parameter value of an individual solution is adjusted during the genetic modification step.
- `crossover_rate`: The probability that a parameter value pair is exchanged between individuals during the genetic modification step.
- `mutation_span`: The expected change of a value during mutation, as a percentage between the lower and upper bounds of the parameter.

#### Optimization Function

The optimization function (also: 'objective', or 'func') is defined by the user and **evaluated** multiple times during optimization with EvoBandits. The user also specifies constraints for the solution space (as decision parameters using the Python API or directly as bounds), as well as the conditions (for example, the simulation budget) for the optimization.

#### Trial

With respect to the Python API, a trial stands for a single evaluation of the optimization function. This is closely connected to the following keywords:
- `trials`: The budget, or number of function evaluations for the optimization.
- `best_trial`: The parameters with the best evaluation result from the optimization.

#### Seeding

The user can define a `seed` to ensure deterministic behaviour and reproduce optimization results (under certain conditions).
Per default, the optimization is unseeded, and system entropy is used instead.
