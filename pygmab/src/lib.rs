use pyo3::prelude::*;
use pyo3::types::PyTuple;

#[pyfunction]
fn call_python_function_with_chosen_arg(py: Python, py_func: PyObject) -> PyResult<i64> {
    let chosen_number: i64 = 3;
    // Call the passed-in Python function with that chosen number
    let args = PyTuple::new(py, &[chosen_number]);
    let result_pyobject = py_func.call1(py, args.unwrap())?;

    // Extract the result back into an i64
    let result: i64 = result_pyobject.extract(py)?;
    Ok(result)
}

/// A Python module implemented in Rust.
#[pymodule]
fn pygmab(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(call_python_function_with_chosen_arg, m)?)?;
    Ok(())
}
