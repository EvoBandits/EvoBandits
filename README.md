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

EvoBandits (Evolutionary Multi-Armed Bandits) is an innovative optimization algorithm designed to tackle stochastic problems with high efficiency. By combining genetic algorithms with multi-armed bandit mechanisms, EvoBandits offers a unique, reinforcement learning-based approach to solving complex, large-scale optimization issues. Whether you're working in operations research, machine learning, or data science, EvoBandits provides a robust, scalable solution for optimizing your stochastic models.

## Usage
To install EvoBandits, add the following to your Cargo.toml file:

```bash
pip install evobandits
```

```python
from evobandits import EvoBandits

def test_function(number: list) -> float:
    # your function here

if __name__ == '__main__':
    bounds = [(-5, 10), (-5, 10)]
    evobandits = EvoBandits(test_function, bounds)
    n_trials = 10000
    result = evobandits.optimize(n_trials)
    print(result)
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you want to change.


## License

tbd

## Credit
Deniz Preil wrote the initial EvoBandits code, which Timo Kühne and Jonathan Laib rewrote.

## Citing EvoBandits

If you use EvoBandits in your research, please cite the following paper:

```
Preil, D., & Krapp, M. (2024). Genetic Multi-Armed Bandits: A Reinforcement Learning Inspired Approach for Simulation Optimization. IEEE Transactions on Evolutionary Computation.
```
