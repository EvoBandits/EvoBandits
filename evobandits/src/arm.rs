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
    action_vector: Vec<i32>,
    reward: f64, // TODO Issue #101: directly track value with Welford's algorithm
    n_evaluations: i32,
}

impl Arm {
    pub fn new(action_vector: &[i32]) -> Self {
        Self {
            reward: 0.0,
            n_evaluations: 0,
            action_vector: action_vector.to_vec(),
        }
    }

    pub(crate) fn pull<F: OptimizationFn>(&mut self, opt_fn: &F) -> f64 {
        let g = opt_fn.evaluate(&self.action_vector);

        self.reward += g;
        self.n_evaluations += 1;

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
        self.reward / self.n_evaluations as f64
    }
}

impl Clone for Arm {
    fn clone(&self) -> Self {
        Self {
            action_vector: self.action_vector.clone(),
            reward: self.reward,
            n_evaluations: self.n_evaluations,
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
    }

    #[test]
    fn test_arm_pull_multiple() {
        let mut arm = Arm::new(&vec![1, 2]);
        arm.pull(&mock_opti_function);
        arm.pull(&mock_opti_function);

        assert_eq!(arm.get_n_evaluations(), 2);
        assert_eq!(arm.get_value(), 5.0); // Since reward is always 5.0
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
    fn test_clone_after_pulls() {
        let mut arm = Arm::new(&vec![1, 2]);
        arm.pull(&mock_opti_function);
        let cloned_arm = arm.clone();
        assert_eq!(arm.get_n_evaluations(), cloned_arm.get_n_evaluations());
        assert_eq!(arm.get_value(), cloned_arm.get_value());
    }
}
