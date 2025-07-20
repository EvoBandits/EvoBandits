// Copyright 2025 EvoBandits
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

use std::hash::{Hash, Hasher};

pub trait OptimizationFn {
    fn evaluate(&self, action_vector: &[i32]) -> f64;
}

impl<F: Fn(&[i32]) -> f64> OptimizationFn for F {
    fn evaluate(&self, action_vector: &[i32]) -> f64 {
        self(action_vector)
    }
}

#[derive(Debug)]
pub struct Arm {
    // Tracks the running mean (`value`) and corrected sum of squares (`corr_ssq`) of observed rewards
    // using Welford’s one‐pass algorithm. On each new reward `g`, we incrementally update:
    //   let delta = g - value;
    //   value += delta / n;
    //   corr_ssq += delta * (g - value);
    // `delta` is the difference between the incoming reward x and the current mean (value),
    // i.e. the instantaneous error used to update both the mean and the corrected sum of squares.
    //
    // This yields a numerically stable estimate of the variance (corr_ssq / (n - 1)) without storing
    // all past samples. It prevents catastrophic cancellation and maintains accuracy in a single pass.
    //
    // Source: Welford, B. P. (1962) ‘Note on a Method for Calculating Corrected Sums of Squares and Products’,
    // Technometrics, 4(3), pp. 419–420. doi: 10.1080/00401706.1962.10490022.
    action_vector: Vec<i32>,
    n_evaluations: i32,
    value: f64,
    corr_ssq: f64,
}

impl Arm {
    pub fn new(action_vector: &[i32]) -> Self {
        Self {
            action_vector: action_vector.to_vec(),
            n_evaluations: 0,
            value: 0.0,
            corr_ssq: 0.0,
        }
    }

    pub(crate) fn pull<F: OptimizationFn>(&mut self, opt_fn: &F) -> f64 {
        let g = opt_fn.evaluate(&self.action_vector);

        // Update Arm according to Welford's algorithm (see above)
        self.n_evaluations += 1;
        let delta = g - self.value;
        self.value += delta / self.n_evaluations as f64;
        self.corr_ssq += delta * (g - self.value);

        g
    }

    pub fn get_n_evaluations(&self) -> i32 {
        self.n_evaluations
    }

    pub(crate) fn get_function_value<F: OptimizationFn>(&self, opt_fn: &F) -> f64 {
        opt_fn.evaluate(&self.action_vector)
    }

    pub fn get_action_vector(&self) -> &[i32] {
        &self.action_vector
    }

    pub fn get_value(&self) -> f64 {
        if self.n_evaluations == 0 {
            return 0.0;
        }
        self.value
    }

    pub fn get_value_std_dev(&self) -> f64 {
        if self.n_evaluations <= 1 {
            return 0.0;
        }
        let variance = self.corr_ssq / (self.n_evaluations - 1) as f64;
        (variance).sqrt()
    }
}

impl Clone for Arm {
    fn clone(&self) -> Self {
        Self {
            action_vector: self.action_vector.clone(),
            n_evaluations: self.n_evaluations,
            value: self.value,
            corr_ssq: self.corr_ssq,
        }
    }
}

impl PartialEq for Arm {
    fn eq(&self, other: &Self) -> bool {
        self.action_vector == other.action_vector
    }
}

impl Eq for Arm {}

impl Hash for Arm {
    fn hash<H: Hasher>(&self, state: &mut H) {
        self.action_vector.hash(state);
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::cell::RefCell;
    use std::rc::Rc;

    // Mock optimization function for testing
    fn mock_opti_function(_vec: &[i32]) -> f64 {
        5.0
    }

    #[test]
    fn test_arm_new() {
        let arm = Arm::new(&vec![1, 2]);
        assert_eq!(arm.get_n_evaluations(), 0);
        assert_eq!(arm.get_function_value(&mock_opti_function), 5.0);
    }

    #[test]
    fn test_arm_pull() {
        let mut arm = Arm::new(&vec![1, 2]);
        let reward = arm.pull(&mock_opti_function);

        assert_eq!(reward, 5.0);
        assert_eq!(arm.get_n_evaluations(), 1);
        assert_eq!(arm.get_value(), 5.0);
        assert_eq!(arm.get_value_std_dev(), 0.0);
    }

    #[test]
    fn test_arm_pull_multiple() {
        let mut arm = Arm::new(&vec![1, 2]);
        arm.pull(&mock_opti_function);
        arm.pull(&mock_opti_function);

        assert_eq!(arm.get_n_evaluations(), 2);
        assert_eq!(arm.get_value(), 5.0); // Since reward is always 5.0
        assert_eq!(arm.get_value_std_dev(), 0.0) // Since reward is always 5.0
    }

    #[test]
    fn test_arm_variance_non_constant_rewards() {
        let values = vec![0.0, 2.0, 4.0];
        let index = Rc::new(RefCell::new(0));

        let variable_fn = {
            let values = values.clone();
            let index = Rc::clone(&index);

            move |_: &[i32]| {
                let i = *index.borrow();
                let val = values[i];
                *index.borrow_mut() += 1;
                val
            }
        };

        let mut arm = Arm::new(&vec![0]);
        arm.pull(&variable_fn);
        arm.pull(&variable_fn);
        arm.pull(&variable_fn);

        // Verify expected sample std_dev of [0, 2, 4]
        assert!((arm.get_value_std_dev() - 2.0).abs() < 1e-10);
    }

    #[test]
    fn test_arm_clone() {
        let arm = Arm::new(&vec![1, 2]);
        let cloned_arm = arm.clone();

        assert_eq!(arm.get_n_evaluations(), cloned_arm.get_n_evaluations());
        assert_eq!(
            arm.get_function_value(&mock_opti_function),
            cloned_arm.get_function_value(&mock_opti_function)
        );
        assert_eq!(arm.get_action_vector(), cloned_arm.get_action_vector());
        assert_eq!(arm.get_value_std_dev(), cloned_arm.get_value_std_dev());
    }

    #[test]
    fn test_initial_reward_is_zero() {
        let arm = Arm::new(&vec![1, 2]);
        assert_eq!(arm.get_value(), 0.0);
    }

    #[test]
    fn test_value_with_zero_pulls() {
        let arm = Arm::new(&vec![1, 2]);
        assert_eq!(arm.get_value(), 0.0);
    }

    #[test]
    fn test_variance_with_zero_pulls() {
        let arm = Arm::new(&vec![1, 2]);
        assert_eq!(arm.get_value_std_dev(), 0.0);
    }

    #[test]
    fn test_clone_after_pulls() {
        let mut arm = Arm::new(&vec![1, 2]);
        arm.pull(&mock_opti_function);
        arm.pull(&mock_opti_function);
        let cloned_arm = arm.clone();
        assert_eq!(arm.get_n_evaluations(), cloned_arm.get_n_evaluations());
        assert_eq!(arm.get_value(), cloned_arm.get_value());
        assert_eq!(arm.get_value_std_dev(), cloned_arm.get_value_std_dev());
    }
}
