<p align="center">
  <img src="Logo.webp" alt="GMAB" width="200"/>
</p>

<p align="center">
<em>GMAB is a cutting-edge optimization algorithm that merges genetic algorithms and multi-armed bandit strategies to efficiently solve stochastic problems.</em>
</p>

---

GMAB (Genetic Multi-Armed Bandits) is an innovative optimization algorithm designed to tackle stochastic problems with high efficiency. By combining genetic algorithms with multi-armed bandit mechanisms, GMAB offers a unique, reinforcement learning-based approach to solving complex, large-scale optimization issues. Whether you're working in operations research, machine learning, or data science, GMAB provides a robust, scalable solution for optimizing your stochastic models.

## Usage
To install GMAB, add the following to your Cargo.toml file:

```toml
[dependencies]
gmab = "0.1.0"
```

```rust
use gmab::GMAB;
use std::f64::consts::PI;

fn ackley_function(x: &[f64]) -> f64 {
    let n = x.len() as f64;
    let sum1: f64 = x.iter().map(|&xi| xi.powi(2)).sum();
    let sum2: f64 = x.iter().map(|&xi| (2.0 * PI * xi).cos()).sum();
    -20.0 * (-0.2 * sum1 / n).sqrt().exp() - (sum2 / n).exp() + 20.0 + std::f64::consts::E
}

fn main() {
    let mut gmab = GMAB::new(ackley_function,
                             20,
                             0.25,
                             1.0,
                             0.1,
                             10000,
                             2,
                             vec![-500, -500],
                             vec![500, 500]);
    let result = gmab.optimize(false);
    println!("Result: {:?}", result);
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.


## License

tbd

## Credit 
GMAB was developed by:

- Deniz Preil
- Timo Kühne
- Jonathan Laib


## Citing GMAB

If you use GMAB in your research, please cite the following paper:

```
PREIL, Deniz; KRAPP, Michael. Genetic multi-armed bandits: a reinforcement learning approach for discrete optimization via simulation. arXiv preprint arXiv:2302.07695, 2023.
```
