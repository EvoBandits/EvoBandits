use pyo3::prelude::*;
use pyo3::types::PyList;

use gmab_rust::arm::OptimizationFn;
use gmab_rust::gmab::Gmab as RustGmab;

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
    fn new(py_func: PyObject, bounds: Vec<(i32, i32)>) -> PyResult<Self> {
        let python_opti_fn = PythonOptimizationFn::new(py_func);
        let gmab = RustGmab::new(python_opti_fn, bounds);
        Ok(Gmab { gmab })
    }

    fn optimize(&mut self, simulation_budget: usize) -> Vec<i32> {
        self.gmab.optimize(simulation_budget)
    }
}

#[pymodule]
fn gmab(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<Gmab>().unwrap();
    Ok(())
}
