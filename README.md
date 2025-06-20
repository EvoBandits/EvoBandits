<p align="center">
  <img src="https://raw.githubusercontent.com/EvoBandits/EvoBandits/refs/heads/main/Logo.webp" alt="EvoBandits" width="200"/>
</p>

<p align="center">
<em>EvoBandits is a cutting-edge optimization algorithm that merges genetic algorithms and multi-armed bandit strategies to efficiently solve stochastic problems.</em>
</p>
<p align="center">
<a href="https://github.com/E-MAB/G-MAB/actions?query=workflow%3ARust+event%3Apush+branch%3Amain" target="_blank">
    <img src="https://github.com/E-MAB/G-MAB/actions/workflows/rust.yml/badge.svg?event=push&branch=main" alt="Build & Test">
</a>
</p>

---

EvoBandits (Evolutionary Multi-Armed Bandits) is an innovative optimization algorithm designed to tackle stochastic problems efficiently. EvoBandits offers a reinforcement learning-based approach to solving complex, large-scale optimization issues by combining genetic algorithms with multi-armed bandit mechanisms. Whether you're working in operations research, machine learning, or data science, EvoBandits provides a robust, scalable solution for optimizing your stochastic models.

## Usage
To install EvoBandits:

```bash
pip install evobandits
```

```python
from evobandits import GMAB

def test_function(number: list) -> float:
    # your function here

if __name__ == '__main__':
    bounds = [(-5, 10), (-5, 10)]
    algorithm = GMAB(test_function, bounds)
    n_trials = 10000
    result = algorithm.optimize(n_trials)
    print(result)
```

## Contributing
Pull requests are welcome. For major changes, please open a discussion first to talk about what you'd like to change.

## License
EvoBandits is licensed under the Apache-2.0 license ([LICENSE](LICENSE) or
<https://opensource.org/licenses/apache-2-0>).

## Credit
Deniz Preil wrote the initial EvoBandits prototype in C++, which Timo Kühne and Jonathan Laib rewrote. Timo Kühne ported to Rust, which is now the backend. Felix Würmseher added the Python frontend.

## Citing EvoBandits
If you use EvoBandits in your research, please cite the following paper:

```
Preil, D., & Krapp, M. (2024). Genetic Multi-Armed Bandits: A Reinforcement Learning Inspired Approach for Simulation Optimization. IEEE Transactions on Evolutionary Computation.
```
