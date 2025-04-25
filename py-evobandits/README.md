## Python Bindings

We use Maturin to build the Python bindings for EvoBandits.

### Installation

```bash
pipx install maturin
```

### Building
To install the Python package into your local environment for development, run the following command:

```bash
maturin develop
```

### Examples
See PyO3/Maturin [Examples](https://github.com/PyO3/maturin?tab=readme-ov-file#examples)

### Why python subdirectory?
Because without we get import errors. more info [here](https://www.maturin.rs/project_layout#mixed-rustpython-project)
