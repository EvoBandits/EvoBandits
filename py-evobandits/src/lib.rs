use pyo3::exceptions::PyRuntimeError;
use pyo3::prelude::*;
use pyo3::types::PyList;
use std::panic;

use evobandits_rust::arm::OptimizationFn;
use evobandits_rust::evobandits::EvoBandits as RustEvoBandits;

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
    #[pyo3(signature = (py_func, bounds, seed=None))]
    fn new(py_func: PyObject, bounds: Vec<(i32, i32)>, seed: Option<u64>) -> PyResult<Self> {
        let python_opti_fn = PythonOptimizationFn::new(py_func);

        match panic::catch_unwind(|| RustEvoBandits::new(python_opti_fn, bounds, seed)) {
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
    Ok(())
}
