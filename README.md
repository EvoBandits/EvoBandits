<p align="center">
  <img src="Logo.webp" alt="GMAB" width="200"/>
</p>

<p align="center">
<em>GMAB is a cutting-edge optimization algorithm that merges genetic algorithms and multi-armed bandit strategies to efficiently solve stochastic problems.</em>
</p>
<p align="center">
<a href="https://github.com/E-MAB/G-MAB/actions?query=workflow%3ARust+event%3Apush+branch%3Amain" target="_blank">
    <img src="https://github.com/E-MAB/G-MAB/actions/workflows/rust.yml/badge.svg?event=push&branch=main" alt="Build & Test">
</a>
</p>

---

GMAB (Genetic Multi-Armed Bandits) is an innovative optimization algorithm designed to tackle stochastic problems with high efficiency. By combining genetic algorithms with multi-armed bandit mechanisms, GMAB offers a unique, reinforcement learning-based approach to solving complex, large-scale optimization issues. Whether you're working in operations research, machine learning, or data science, GMAB provides a robust, scalable solution for optimizing your stochastic models.

## Usage
To install GMAB, add the following to your Cargo.toml file:

```toml
[dependencies]
gmab = { git = "https://github.com/E-MAB/G-MAB.git" }
```

```rust
use gmab::gmab::Gmab;

fn your_function(x: &[f64]) -> f64 {
    // your function here
}

fn main() {
    let bounds = vec![(1, 100), (1, 100)];
    let mut gmab = Gmab::new(your_function, bounds);
    let evaluation_budget = 10000;
    let result = gmab.optimize(eval_budget);
    println!("Result: {:?}", result);
}
```

```python
from gmab import Gmab

def test_function(number: list) -> float:
    # your function here

if __name__ == '__main__':
    bounds = [(-5, 10), (-5, 10)]
    gmab = Gmab(test_function, bounds)
    evaluation_budget = 10000
    result = gmab.optimize(evaluation_budget)
    print(result)
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you want to change.


## License

tbd

## Credit
Deniz Preil wrote the initial GMAB code, which Timo Kühne and Jonathan Laib rewrote.

## Citing GMAB

If you use GMAB in your research, please cite the following paper:

```
Preil, D., & Krapp, M. (2024). Genetic Multi-Armed Bandits: A Reinforcement Learning Inspired Approach for Simulation Optimization. IEEE Transactions on Evolutionary Computation.
```
