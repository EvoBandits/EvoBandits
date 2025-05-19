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
pub(crate) struct Arm {
    action_vector: Vec<i32>,
    num_pulls: i32,
    mean_reward: f64,
    corr_ssq: f64,
}

impl Arm {
    pub(crate) fn new(action_vector: &[i32]) -> Self {
        Self {
            num_pulls: 0,
            mean_reward: 0.0,
            corr_ssq: 0.0,
            action_vector: action_vector.to_vec(),
        }
    }

    pub(crate) fn pull<F: OptimizationFn>(&mut self, opt_fn: &F) -> f64 {
        let g = opt_fn.evaluate(&self.action_vector);

        // Update number of pulls
        self.num_pulls += 1;

        // Update sample mean
        let delta = g - self.mean_reward;
        self.mean_reward += delta / self.num_pulls as f64;

        // Update corrected sum of squares (Welford's Method for online variance calculation)
        let delta2 = g - self.mean_reward;
        self.corr_ssq += delta * delta2;

        g
    }

    pub(crate) fn get_num_pulls(&self) -> i32 {
        self.num_pulls
    }

    pub(crate) fn get_function_value<F: OptimizationFn>(&self, opt_fn: &F) -> f64 {
        opt_fn.evaluate(&self.action_vector)
    }

    pub(crate) fn get_action_vector(&self) -> &[i32] {
        &self.action_vector
    }

    pub(crate) fn get_mean_reward(&self) -> f64 {
        if self.num_pulls == 0 {
            return 0.0;
        }
        self.mean_reward
    }

    pub(crate) fn get_variance(&self) -> f64 {
        if self.num_pulls <= 1 {
            return 0.0;
        }
        self.corr_ssq / (self.num_pulls - 1) as f64
    }
}

impl Clone for Arm {
    fn clone(&self) -> Self {
        Self {
            action_vector: self.action_vector.clone(),
            num_pulls: self.num_pulls,
            mean_reward: self.mean_reward,
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
        assert_eq!(arm.get_num_pulls(), 0);
        assert_eq!(arm.get_function_value(&mock_opti_function), 5.0);
    }

    #[test]
    fn test_arm_pull() {
        let mut arm = Arm::new(&vec![1, 2]);
        let reward = arm.pull(&mock_opti_function);

        assert_eq!(reward, 5.0);
        assert_eq!(arm.get_num_pulls(), 1);
        assert_eq!(arm.get_mean_reward(), 5.0);
    }

    #[test]
    fn test_arm_pull_multiple() {
        let mut arm = Arm::new(&vec![1, 2]);
        arm.pull(&mock_opti_function);
        arm.pull(&mock_opti_function);

        assert_eq!(arm.get_num_pulls(), 2);
        assert_eq!(arm.get_mean_reward(), 5.0); // Since reward is always 5.0
        assert_eq!(arm.get_variance(), 0.0) // Since reward is always 5.0
    }

    #[test]
    fn test_arm_variance_non_constant_rewards() {
        let rewards = vec![1.0, 2.0, 3.0];
        let index = Rc::new(RefCell::new(0));

        let variable_fn = {
            let rewards = rewards.clone();
            let index = Rc::clone(&index);

            move |_: &[i32]| {
                let i = *index.borrow();
                let val = rewards[i];
                *index.borrow_mut() += 1;
                val
            }
        };

        let mut arm = Arm::new(&vec![0]);
        arm.pull(&variable_fn);
        arm.pull(&variable_fn);
        arm.pull(&variable_fn);

        let expected_variance = 1.0; // sample variance of [1,2,3]
        assert!((arm.get_variance() - expected_variance).abs() < 1e-10);
    }

    #[test]
    fn test_arm_clone() {
        let arm = Arm::new(&vec![1, 2]);
        let cloned_arm = arm.clone();

        assert_eq!(arm.get_num_pulls(), cloned_arm.get_num_pulls());
        assert_eq!(
            arm.get_function_value(&mock_opti_function),
            cloned_arm.get_function_value(&mock_opti_function)
        );
        assert_eq!(arm.get_action_vector(), cloned_arm.get_action_vector());
        assert_eq!(arm.get_variance(), cloned_arm.get_variance());
    }

    #[test]
    fn test_initial_reward_is_zero() {
        let arm = Arm::new(&vec![1, 2]);
        assert_eq!(arm.get_mean_reward(), 0.0);
    }

    #[test]
    fn test_mean_reward_with_zero_pulls() {
        let arm = Arm::new(&vec![1, 2]);
        assert_eq!(arm.get_mean_reward(), 0.0);
    }

    #[test]
    fn test_variance_with_zero_pulls() {
        let arm = Arm::new(&vec![1, 2]);
        assert_eq!(arm.get_variance(), 0.0);
    }

    #[test]
    fn test_clone_after_pulls() {
        let mut arm = Arm::new(&vec![1, 2]);
        arm.pull(&mock_opti_function);
        arm.pull(&mock_opti_function);
        let cloned_arm = arm.clone();
        assert_eq!(arm.get_num_pulls(), cloned_arm.get_num_pulls());
        assert_eq!(arm.get_mean_reward(), cloned_arm.get_mean_reward());
        assert_eq!(arm.get_variance(), cloned_arm.get_variance());
    }
}
