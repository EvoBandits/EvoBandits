use pyo3::exceptions::PyRuntimeError;
use pyo3::prelude::*;
use pyo3::types::PyList;
use std::panic;

use evobandits_rust::arm::OptimizationFn;
use evobandits_rust::evobandits::EvoBandits as RustEvoBandits;
use evobandits_rust::genetic::{
    CROSSOVER_RATE_DEFAULT, MUTATION_RATE_DEFAULT, MUTATION_SPAN_DEFAULT, POPULATION_SIZE_DEFAULT,
};
use evobandits_rust::gmab_options::GmabOptions;

struct PythonOptimizationFn {
    py_func: PyObject,
}

impl PythonOptimizationFn {
    fn new(py_func: PyObject) -> Self {
        Self { py_func }
    }
}

impl OptimizationFn for PythonOptimizationFn {
    fn evaluate(&self, action_vector: &[i32]) -> f64 {
        Python::with_gil(|py| {
            let py_list = PyList::new(py, action_vector);
            let result = self
                .py_func
                .call1(py, (py_list.unwrap(),))
                .expect("Failed to call Python function");
            result.extract::<f64>(py).expect("Failed to extract f64")
        })
    }
}

#[pyclass]
struct EvoBandits {
    evobandits: RustEvoBandits<PythonOptimizationFn>,
}

#[pymethods]
impl EvoBandits {
    #[new]
    #[pyo3(signature = (
        py_func,
        bounds,
        seed=None,
        population_size=POPULATION_SIZE_DEFAULT,
        mutation_rate=MUTATION_RATE_DEFAULT,
        crossover_rate=CROSSOVER_RATE_DEFAULT,
        mutation_span=MUTATION_SPAN_DEFAULT,
    ))]
    fn new(
        py_func: PyObject,
        bounds: Vec<(i32, i32)>,
        seed: Option<u64>,
        population_size: Option<usize>, // Check if option is needed!
        mutation_rate: Option<f64>,
        crossover_rate: Option<f64>,
        mutation_span: Option<f64>,
    ) -> PyResult<Self> {
        let python_opti_fn = PythonOptimizationFn::new(py_func);

        let options = GmabOptions {
            population_size: population_size.unwrap(),
            mutation_rate: mutation_rate.unwrap(),
            crossover_rate: crossover_rate.unwrap(),
            mutation_span: mutation_span.unwrap(),
            seed: seed,
        };

        match panic::catch_unwind(|| RustEvoBandits::new(python_opti_fn, bounds, options)) {
            Ok(evobandits) => Ok(EvoBandits { evobandits }),
            Err(err) => {
                let err_message = if let Some(msg) = err.downcast_ref::<&str>() {
                    format!("evobandits core raised an exception: {}", msg)
                } else if let Some(msg) = err.downcast_ref::<String>() {
                    format!("evobandits core raised an exception: {}", msg)
                } else {
                    "evobandits core raised an exception (unknown cause)".to_string()
                };
                Err(PyRuntimeError::new_err(err_message))
            }
        }
    }

    fn optimize(&mut self, simulation_budget: usize) -> Vec<i32> {
        self.evobandits.optimize(simulation_budget)
    }
}

#[pymodule]
fn evobandits(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<EvoBandits>()?;

    m.add("POPULATION_SIZE_DEFAULT", POPULATION_SIZE_DEFAULT)?;
    m.add("MUTATION_RATE_DEFAULT", MUTATION_RATE_DEFAULT)?;
    m.add("CROSSOVER_RATE_DEFAULT", CROSSOVER_RATE_DEFAULT)?;
    m.add("MUTATION_SPAN_DEFAULT", MUTATION_SPAN_DEFAULT)?;

    Ok(())
}
