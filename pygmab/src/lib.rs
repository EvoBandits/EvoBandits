use pyo3::exceptions::PyRuntimeError;
use pyo3::prelude::*;
use pyo3::types::PyList;
use std::panic;

use gmab_rust::arm::OptimizationFn;
use gmab_rust::gmab::Gmab as RustGmab;
use gmab_rust::gmab_options::{
    GmabOptions, CROSSOVER_RATE_DEFAULT, MUTATION_RATE_DEFAULT, MUTATION_SPAN_DEFAULT,
    POPULATION_SIZE_DEFAULT,
};

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
struct Gmab {
    gmab: RustGmab<PythonOptimizationFn>,
}

#[pymethods]
impl Gmab {
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
        population_size: Option<usize>,
        mutation_rate: Option<f64>,
        crossover_rate: Option<f64>,
        mutation_span: Option<f64>,
    ) -> PyResult<Self> {
        let python_opti_fn = PythonOptimizationFn::new(py_func);

        // ToDo: Fix the issue where an error here would fail to raise a panic
        let options = GmabOptions::new()
            .with_population_size(population_size.unwrap())
            .with_mutation_rate(mutation_rate.unwrap())
            .with_mutation_span(mutation_span.unwrap())
            .with_crossover_rate(crossover_rate.unwrap())
            .with_mutation_span(mutation_span.unwrap());

        match panic::catch_unwind(|| RustGmab::new(python_opti_fn, bounds, seed, options)) {
            Ok(gmab) => Ok(Gmab { gmab }),
            Err(err) => {
                let err_message = if let Some(msg) = err.downcast_ref::<&str>() {
                    format!("gmab core raised an exception: {}", msg)
                } else if let Some(msg) = err.downcast_ref::<String>() {
                    format!("gmab core raised an exception: {}", msg)
                } else {
                    "gmab core raised an exception (unknown cause)".to_string()
                };
                Err(PyRuntimeError::new_err(err_message))
            }
        }
    }

    fn optimize(&mut self, simulation_budget: usize) -> Vec<i32> {
        self.gmab.optimize(simulation_budget)
    }
}

#[pymodule]
fn gmab(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<Gmab>()?;

    m.add("POPULATION_SIZE_DEFAULT", POPULATION_SIZE_DEFAULT)?;
    m.add("MUTATION_RATE_DEFAULT", MUTATION_RATE_DEFAULT)?;
    m.add("CROSSOVER_RATE_DEFAULT", CROSSOVER_RATE_DEFAULT)?;
    m.add("MUTATION_SPAN_DEFAULT", MUTATION_SPAN_DEFAULT)?;

    Ok(())
}
