# 📘 Glossary

This glossary provides definitions of key terms related to the EvoBandits repository.
It is intended as a quick reference for contributors and users.

---

## Terms

#### Action vector

A discrete, integer decision vector that represents a distinct solution of the optimization problem. For integer decision problems with one decision parameter, the action vector is identical to the respective solution vector. For other problems that are modeled with the Python API, the action vector contains the value representations for all decision parameters. It can be transformed into the solution with encoding/decoding.

#### Bounds

Bounds are defined as a list of tuples, where each tuple specifies the lower and upper limits for a value in the action vector. These bounds constrain the solution space for optimization with EvoBandits. When using the Python API, the bounds are derived from the specifications of the individual decision parameters that make up the action vector.

#### Encoding / Decoding

If the user defines a solution space using the Python API, an encoding step is necessary to convert the solution to an action vector that is usable for optimization with EvoBandits. This step is trivial for integer parameters; however, a discretization step (converting continuous values into discrete intervals) for float parameters and label encoding (assigning unique integer values to categorical data) for categorical parameters is required.

#### EvoBandits Algorithm Options

The user can modify the conditions for the optimization using the following keywords:
- `population_size`: The number of starting solutions, and the number of individual solutions in a generation.
- `mutation_rate`: The probability that a parameter value of an individual solution is adjusted during the genetic modification step.
- `crossover_rate`: The probability that a parameter value pair is exchanged between individuals during the genetic modification step.
- `mutation_span`: The expected change of a value during mutation, as a percentage between the lower and upper bounds of the parameter.

#### Optimization Function

The optimization function (also: 'objective', or 'func') is defined by the user and **evaluated** multiple times during optimization with EvoBandits. The user also specifies constraints for the solution space (as decision parameters using the Python API or directly as bounds), as well as the conditions for the optimization:
- The budget, or number of function evaluations before the optimization stops is set using `n_trials`. A trial stands for a single evaluation of the optimization function.

#### Results

In the context of EvoBandits, a multi-armed bandit algorithm, each result is internally represented by an `Arm`. During optimization, each arm is pulled, i.e. the result is chosen by the algorithm, evaluated with the objective function, and its value is observed and saved. After optimization, the best results are returned.

Users can assess distinct results with the following metrics:
- `params`: The distinct parameter configuration for the result.
- `value`: The objective value of the result observed during optimization. In the case of the EvoBandits algorithm, the value is the mean of all evaluation results.
- `n_evaluations`: The number of times a result has been evaluated during optimization. This metric tracks how much experience the algorithm has with each result (or Arm) and indicates whether a result has been explored or exploited by the algorithm.
- `n_best`: The rank of the result in the respective optimization run. The best configuration is marked with n_best = 1.

#### Seeding

The user can define a `seed` to ensure deterministic behaviour and reproduce optimization results (under certain conditions).
Per default, the optimization is unseeded, and system entropy is used instead.
