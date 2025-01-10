use pyo3::prelude::*;
use pyo3::types::PyList;

use gmab::arm::OptimizationFn;
use gmab::gmab::Gmab;

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

#[pyfunction]
fn optimizer(
    py_func: PyObject,
    bounds: Vec<(i32, i32)>,
    simulation_budget: usize,
) -> PyResult<Vec<i32>> {
    let python_opti_fn = PythonOptimizationFn::new(py_func);

    let mut gmab = Gmab::new(python_opti_fn, bounds);

    let best_solution = gmab.optimize(simulation_budget);

    Ok(best_solution)
}

#[pymodule]
fn pygmab(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(optimizer, m)?)?;
    Ok(())
}
