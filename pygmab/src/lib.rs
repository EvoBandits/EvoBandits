use pyo3::prelude::*;
use pyo3::types::PyList;

#[pyfunction]
fn call_python_function_with_chosen_arg(py: Python, py_func: PyObject) -> PyResult<i64> {
    let elements: Vec<i32> = vec![0, 1, 2, 3, 4, 0];
    let list = PyList::new(py, elements)?;

    let result_pyobject = py_func.call1(py, (list,))?;

    let result: i64 = result_pyobject.extract(py)?;
    Ok(result)
}

/// A Python module implemented in Rust.
#[pymodule]
fn pygmab(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(call_python_function_with_chosen_arg, m)?)?;
    Ok(())
}
