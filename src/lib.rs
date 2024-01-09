use std::cmp::Ordering;
use std::collections::{BTreeMap, HashMap};

use arm::Arm;
use genetic::GeneticAlgorithm;

use crate::arm::OptimizationFn;

mod arm;
mod genetic;

#[derive(Debug, PartialEq, PartialOrd, Clone, Copy)]
struct FloatKey(f64);

impl Eq for FloatKey {}

impl Ord for FloatKey {
    fn cmp(&self, other: &Self) -> Ordering {
        self.partial_cmp(other).unwrap_or(Ordering::Less)
    }
}

#[derive(Debug)]
struct SortedMultiMap<K: Ord, V: PartialEq> {
    inner: BTreeMap<K, Vec<V>>,
}

impl<K: Ord, V: PartialEq> SortedMultiMap<K, V> {
    pub fn new() -> Self {
        SortedMultiMap {
            inner: BTreeMap::new(),
        }
    }

    pub fn insert(&mut self, key: K, value: V) {
        self.inner.entry(key).or_insert_with(Vec::new).push(value);
    }

    pub fn delete(&mut self, key: &K, value: &V) -> bool {
        if let Some(values) = self.inner.get_mut(key) {
            if let Some(pos) = values.iter().position(|v| v == value) {
                values.remove(pos);
                if values.is_empty() {
                    self.inner.remove(key);
                }
                return true;
            }
        }
        false
    }

    pub fn iter(&self) -> impl Iterator<Item = (&K, &V)> {
        self.inner
            .iter()
            .flat_map(|(key, values)| values.iter().map(move |value| (key, value)))
    }
}

pub struct Gmab<F: OptimizationFn> {
    sample_average_tree: SortedMultiMap<FloatKey, i32>,
    arm_memory: Vec<Arm<F>>,
    lookup_table: HashMap<Vec<i32>, i32>,
    genetic_algorithm: GeneticAlgorithm<F>,
    current_indexes: Vec<i32>,
}

impl<F: OptimizationFn + Clone> Gmab<F> {
    fn get_arm_index(&self, individual: &Arm<F>) -> i32 {
        match self
            .lookup_table
            .get(&individual.get_action_vector().to_vec())
        {
            Some(&index) => index,
            None => -1,
        }
    }

    pub fn new(
        opti_function: F,
        population_size: usize,
        mutation_rate: f64,
        crossover_rate: f64,
        mutation_span: f64,
        max_simulations: i32,
        dimension: usize,
        lower_bound: Vec<i32>,
        upper_bound: Vec<i32>,
    ) -> Gmab<F> {
        let mut genetic_algorithm = GeneticAlgorithm::new(
            opti_function,
            population_size,
            mutation_rate,
            crossover_rate,
            mutation_span,
            max_simulations,
            dimension,
            lower_bound,
            upper_bound,
        );

        let mut arm_memory: Vec<Arm<F>> = Vec::new();
        let mut lookup_table: HashMap<Vec<i32>, i32> = HashMap::new();
        let mut sample_average_tree: SortedMultiMap<FloatKey, i32> = SortedMultiMap::new();

        for (index, individual) in genetic_algorithm.get_individuals().iter_mut().enumerate() {
            individual.pull();
            arm_memory.push(individual.clone());
            lookup_table.insert(individual.get_action_vector().to_vec(), index as i32);
            sample_average_tree.insert(FloatKey(individual.get_mean_reward()), index as i32);
        }

        Gmab {
            sample_average_tree,
            arm_memory,
            lookup_table,
            genetic_algorithm,
            current_indexes: Vec::new(),
        }
    }

    fn max_number_pulls(&self) -> i32 {
        let mut max_number_pulls = 0;
        for arm in &self.arm_memory {
            if arm.get_num_pulls() > max_number_pulls {
                max_number_pulls = arm.get_num_pulls();
            }
        }
        max_number_pulls
    }

    fn find_best_ucb(&self) -> i32 {
        let arm_index_ucb_norm_min: i32 = *self.sample_average_tree.iter().next().unwrap().1;
        let ucb_norm_min: f64 = self.arm_memory[arm_index_ucb_norm_min as usize].get_mean_reward();

        let max_number_pulls = self.max_number_pulls();

        let mut ucb_norm_max: f64 = ucb_norm_min;

        for (_ucb_norm, arm_index) in self.sample_average_tree.iter() {
            ucb_norm_max = f64::max(
                ucb_norm_max,
                self.arm_memory[*arm_index as usize].get_mean_reward(),
            );

            // checks if we are still in the non dominated-set (current mean <= mean_max_pulls)
            if self.arm_memory[*arm_index as usize].get_num_pulls() == max_number_pulls {
                break;
            }
        }

        // find the solution of non-dominated set with the lowest associated UCB value
        let mut best_arm_index: i32 = 0;
        let mut best_ucb_value: f64 = f64::MAX;

        for (_ucb_norm, arm_index) in self.sample_average_tree.iter() {
            if ucb_norm_max == ucb_norm_min {
                best_arm_index = *arm_index;
            }

            // transform sample mean to interval [0,1]
            let transformed_sample_mean: f64 =
                (self.arm_memory[*arm_index as usize].get_mean_reward() - ucb_norm_min)
                    / (ucb_norm_max - ucb_norm_min);
            let penalty_term: f64 = (2.0
                * (self.genetic_algorithm.get_simulations_used() as f64).ln()
                / self.arm_memory[*arm_index as usize].get_num_pulls() as f64)
                .sqrt();
            let ucb_value: f64 = transformed_sample_mean + penalty_term;

            // new best solution found
            if ucb_value < best_ucb_value {
                best_arm_index = *arm_index;
                best_ucb_value = ucb_value;
            }

            // checks if we are still in the non dominated-set (current mean <= mean_max_pulls)
            if self.arm_memory[*arm_index as usize].get_num_pulls() == max_number_pulls {
                break;
            }
        }

        best_arm_index
    }

    fn sample_and_update(&mut self, arm_index: i32, mut individual: Arm<F>) {
        if arm_index >= 0 {
            self.sample_average_tree.delete(
                &FloatKey(self.arm_memory[arm_index as usize].get_mean_reward()),
                &arm_index,
            );
            self.arm_memory[arm_index as usize].pull();
            self.genetic_algorithm.update_simulations_used(1);
            self.sample_average_tree.insert(
                FloatKey(self.arm_memory[arm_index as usize].get_mean_reward()),
                arm_index,
            );
        } else {
            individual.pull();
            self.genetic_algorithm.update_simulations_used(1);
            self.arm_memory.push(individual.clone());
            self.lookup_table.insert(
                individual.get_action_vector().to_vec(),
                self.arm_memory.len() as i32 - 1,
            );
            self.sample_average_tree.insert(
                FloatKey(individual.get_mean_reward()),
                self.arm_memory.len() as i32 - 1,
            );
        }
    }

    pub fn optimize(&mut self, verbose: bool) -> Vec<i32> {
        loop {
            self.genetic_algorithm.get_individuals().clear();
            self.current_indexes.clear();

            // get first self.population_size elements from sorted tree and use value to get arm
            self.sample_average_tree
                .iter()
                .take(self.genetic_algorithm.get_population_size())
                .for_each(|(_key, arm_index)| {
                    self.genetic_algorithm
                        .get_individuals()
                        .push(self.arm_memory[*arm_index as usize].clone());
                    self.current_indexes.push(*arm_index);
                });

            // shuffle population
            self.genetic_algorithm.shuffle_population();

            let crossover_pop = self.genetic_algorithm.crossover();

            // mutate automatically removes duplicates
            let mutated_pop = self.genetic_algorithm.mutate(&crossover_pop);

            for individual in mutated_pop {
                let arm_index = self.get_arm_index(&individual);

                // check if arm is in current population
                if self.current_indexes.contains(&arm_index) {
                    continue;
                }

                self.sample_and_update(arm_index, individual.clone());

                if self.genetic_algorithm.budget_reached() {
                    return self.arm_memory[self.find_best_ucb() as usize]
                        .get_action_vector()
                        .to_vec();
                }
            }

            let individuals = self.genetic_algorithm.get_individuals().clone();

            for individual in individuals {
                let arm_index = self.get_arm_index(&individual);
                self.sample_and_update(arm_index, individual.clone());

                if self.genetic_algorithm.budget_reached() {
                    return self.arm_memory[self.find_best_ucb() as usize]
                        .get_action_vector()
                        .to_vec();
                }
            }

            if verbose {
                let best_arm_index = self.find_best_ucb();
                print!(
                    "x: {:?}",
                    self.arm_memory[best_arm_index as usize].get_action_vector()
                );
                // get averaged function value over 50 simulations
                let mut sum = 0.0;
                for _ in 0..50 {
                    sum += self.arm_memory[best_arm_index as usize].get_function_value();
                }
                print!(" f(x): {:.3}", sum / 50.0);

                print!(" n: {}", self.genetic_algorithm.get_simulations_used());
                // print number of pulls of best arm
                println!(
                    " n(x): {}",
                    self.arm_memory[best_arm_index as usize].get_num_pulls()
                );
            }
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_sorted_multi_map_insert() {
        let mut map = SortedMultiMap::new();
        map.insert(FloatKey(1.0), 1);
        map.insert(FloatKey(1.0), 2);
        map.insert(FloatKey(2.0), 3);

        let mut iter = map.iter();

        assert_eq!(iter.next(), Some((&FloatKey(1.0), &1)));
        assert_eq!(iter.next(), Some((&FloatKey(1.0), &2)));
        assert_eq!(iter.next(), Some((&FloatKey(2.0), &3)));
        assert_eq!(iter.next(), None);
    }

    #[test]
    fn test_sorted_multi_map_delete() {
        let mut map = SortedMultiMap::new();
        map.insert(FloatKey(1.0), 1);
        map.insert(FloatKey(1.0), 2);
        map.insert(FloatKey(2.0), 3);

        assert!(map.delete(&FloatKey(1.0), &1));
        assert!(map.delete(&FloatKey(2.0), &3));
        assert!(!map.delete(&FloatKey(2.0), &3));

        let mut iter = map.iter();

        assert_eq!(iter.next(), Some((&FloatKey(1.0), &2)));
        assert_eq!(iter.next(), None);
    }

    fn mock_opti_function(_vec: &[i32]) -> f64 {
        0.0
    }

    #[test]
    fn test_gmab_new() {
        let gmab = Gmab::new(
            mock_opti_function,
            10,
            0.1,
            0.9,
            0.5,
            100,
            2,
            vec![0, 0],
            vec![10, 10],
        );
        assert_eq!(gmab.genetic_algorithm.get_population_size(), 10);
        assert_eq!(gmab.arm_memory.len(), 10);
        assert_eq!(gmab.lookup_table.len(), 10);

        // check if there are 10  elements in sample_average_tree
        let mut count = 0;
        for _ in gmab.sample_average_tree.iter() {
            count += 1;
        }
        assert_eq!(count, 10);
    }

    #[test]
    fn test_gmab_get_arm_index_with_existing() {
        let mut gmab = Gmab::new(
            mock_opti_function,
            10,
            0.1,
            0.9,
            0.5,
            100,
            2,
            vec![0, 0],
            vec![10, 10],
        );
        let arm = Arm::new(mock_opti_function, &vec![1, 2]);
        gmab.arm_memory.push(arm.clone());
        gmab.lookup_table
            .insert(arm.get_action_vector().to_vec(), 0);
        assert_eq!(gmab.get_arm_index(&arm), 0);
    }

    #[test]
    fn test_gmab_max_number_pulls() {
        let gmab = Gmab::new(
            mock_opti_function,
            10,
            0.1,
            0.9,
            0.5,
            100,
            2,
            vec![0, 0],
            vec![10, 10],
        );
        assert_eq!(gmab.max_number_pulls(), 1);
    }

    #[test]
    fn test_gmab_find_best_ucb() {
        let gmab = Gmab::new(
            mock_opti_function,
            10,
            0.1,
            0.9,
            0.5,
            100,
            2,
            vec![0, 0],
            vec![10, 10],
        );
        assert_eq!(gmab.find_best_ucb(), 0);
    }

    #[test]
    fn test_gmab_find_best_ucb_with_existing() {
        let mut gmab = Gmab::new(
            mock_opti_function,
            10,
            0.1,
            0.9,
            0.5,
            100,
            2,
            vec![0, 0],
            vec![10, 10],
        );

        let arm = Arm::new(mock_opti_function, &vec![1, 2]);
        gmab.arm_memory.push(arm.clone());
        gmab.lookup_table
            .insert(arm.get_action_vector().to_vec(), 0);

        let arm2 = Arm::new(mock_opti_function, &vec![1, 2]);
        gmab.arm_memory.push(arm2.clone());
        gmab.lookup_table
            .insert(arm2.get_action_vector().to_vec(), 1);

        gmab.sample_and_update(0, arm.clone());
        gmab.sample_and_update(1, arm2.clone());

        assert_eq!(gmab.find_best_ucb(), 0);
    }

    #[test]
    fn test_gmab_sample_and_update_with_existing() {
        let mut gmab = Gmab::new(
            mock_opti_function,
            10,
            0.1,
            0.9,
            0.5,
            100,
            2,
            vec![0, 0],
            vec![10, 10],
        );

        let arm = Arm::new(mock_opti_function, &vec![1, 2]);
        gmab.arm_memory.push(arm.clone());
        gmab.lookup_table
            .insert(arm.get_action_vector().to_vec(), 0);

        gmab.sample_and_update(0, arm.clone());

        assert_eq!(gmab.arm_memory[0].get_num_pulls(), 2);
        assert_eq!(gmab.arm_memory[0].get_mean_reward(), 0.0);
        assert_eq!(
            gmab.lookup_table.get(&arm.get_action_vector().to_vec()),
            Some(&0)
        );
    }
}
