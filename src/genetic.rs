use std::collections::HashSet;

use rand::seq::SliceRandom;
use rand::Rng;
use rand_distr::{Distribution, Normal};

use crate::arm::{Arm, OptimizationFn};

pub(crate) struct GeneticAlgorithm<F: OptimizationFn> {
    mutation_rate: f64,
    crossover_rate: f64,
    mutation_span: f64,
    population_size: usize,
    individuals: Vec<Arm<F>>,
    pub(crate) opti_function: F,
    max_simulations: i32,
    dimension: usize,
    lower_bound: Vec<i32>,
    upper_bound: Vec<i32>,
    simulations_used: i32,
}

impl<F: OptimizationFn + Clone> GeneticAlgorithm<F> {
    pub(crate) fn get_population_size(&self) -> usize {
        self.population_size
    }

    pub(crate) fn get_individuals(&mut self) -> &mut Vec<Arm<F>> {
        &mut self.individuals
    }

    pub(crate) fn get_simulations_used(&self) -> i32 {
        self.simulations_used
    }

    pub(crate) fn update_simulations_used(&mut self, number_of_new_simulations: i32) {
        self.simulations_used += number_of_new_simulations;
    }

    pub(crate) fn budget_reached(&self) -> bool {
        self.simulations_used >= self.max_simulations
    }

    pub(crate) fn new(
        opti_function: F,
        population_size: usize,
        mutation_rate: f64,
        crossover_rate: f64,
        mutation_span: f64,
        max_simulations: i32,
        dimension: usize,
        lower_bound: Vec<i32>,
        upper_bound: Vec<i32>,
    ) -> Self {
        let mut individuals: Vec<Arm<F>> = Vec::new();
        let mut init_solutions: Vec<Vec<i32>> = Vec::new();

        for _ in 0..population_size {
            let action_vector = Self::generate_unique_solution(
                &init_solutions,
                &lower_bound,
                &upper_bound,
                dimension,
            );
            init_solutions.push(action_vector.clone());
            individuals.push(Arm::new(opti_function.clone(), &action_vector));
        }

        Self {
            mutation_rate,
            crossover_rate,
            mutation_span,
            population_size,
            individuals,
            opti_function,
            max_simulations,
            dimension,
            lower_bound,
            upper_bound,
            simulations_used: 0,
        }
    }

    fn generate_unique_solution(
        existing_solutions: &[Vec<i32>],
        lower_bound: &[i32],
        upper_bound: &[i32],
        dimension: usize,
    ) -> Vec<i32> {
        let mut rng = rand::thread_rng();

        loop {
            let candidate_solution: Vec<i32> = (0..dimension)
                .map(|j| rng.gen_range(lower_bound[j]..=upper_bound[j]))
                .collect();

            if !existing_solutions.contains(&candidate_solution) {
                return candidate_solution;
            }
        }
    }

    pub(crate) fn shuffle_population(&mut self) {
        let mut rng = rand::thread_rng();
        self.individuals.shuffle(&mut rng);
    }

    pub(crate) fn crossover(&self) -> Vec<Arm<F>> {
        let mut crossover_pop: Vec<Arm<F>> = Vec::new();
        let population_size = self.get_population_size();

        for i in (0..population_size).step_by(2) {
            if rand::random::<f64>() < self.crossover_rate {
                // Crossover
                let max_dim_index = self.dimension - 1;
                let swap_rv = rand::random::<usize>() % max_dim_index + 1;

                for j in 1..=max_dim_index {
                    if swap_rv == j {
                        let mut cross_vec_1: Vec<i32> =
                            self.individuals[i].get_action_vector()[0..j].to_vec();
                        cross_vec_1.extend_from_slice(
                            &self.individuals[i + 1].get_action_vector()[j..=max_dim_index],
                        );

                        let mut cross_vec_2: Vec<i32> =
                            self.individuals[i + 1].get_action_vector()[0..j].to_vec();
                        cross_vec_2.extend_from_slice(
                            &self.individuals[i].get_action_vector()[j..=max_dim_index],
                        );

                        let new_individual_1 = Arm::new(self.opti_function.clone(), &cross_vec_1);
                        let new_individual_2 = Arm::new(self.opti_function.clone(), &cross_vec_2);

                        crossover_pop.push(new_individual_1);
                        crossover_pop.push(new_individual_2);
                    }
                }
            } else {
                // No Crossover
                crossover_pop.push(self.individuals[i].clone()); // Assuming your Arm struct implements the Clone trait
                crossover_pop.push(self.individuals[i + 1].clone()); // Assuming your Arm struct implements the Clone trait
            }
        }

        crossover_pop
    }

    pub(crate) fn mutate(&self, population: &[Arm<F>]) -> Vec<Arm<F>> {
        let mut mutated_population = Vec::new();
        let mut seen = HashSet::new();
        let mut rng = rand::thread_rng();

        for individual in population.iter() {
            // Clone the action vector
            let mut new_action_vector = individual.get_action_vector().to_vec(); // Here I assumed `get_action_vector` returns a slice or Vec

            for (i, value) in new_action_vector.iter_mut().enumerate() {
                if rng.gen::<f64>() < self.mutation_rate {
                    let adjustment = Normal::new(
                        0.0,
                        self.mutation_span * (self.upper_bound[i] - self.lower_bound[i]) as f64,
                    )
                    .unwrap()
                    .sample(&mut rng);

                    *value = (*value as f64 + adjustment)
                        .max(self.lower_bound[i] as f64)
                        .min(self.upper_bound[i] as f64) as i32;
                }
            }

            let new_individual = Arm::new(individual.arm_fn.clone(), new_action_vector.as_slice());

            if seen.insert(new_individual.clone()) {
                mutated_population.push(new_individual);
            }
        }

        mutated_population
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    // Mock optimization function for testing
    fn mock_opti_function(_vec: &[i32]) -> f64 {
        0.0
    }

    #[test]
    fn test_get_population_size() {
        let ga = GeneticAlgorithm::new(
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
        assert_eq!(ga.get_population_size(), 10);
    }

    #[test]
    fn test_get_individuals() {
        let mut ga = GeneticAlgorithm::new(
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
        assert_eq!(ga.get_individuals().len(), 10);
    }

    #[test]
    fn test_get_simulations_used() {
        let ga = GeneticAlgorithm::new(
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
        assert_eq!(ga.get_simulations_used(), 0);
    }

    #[test]
    fn test_update_simulations_used() {
        let mut ga = GeneticAlgorithm::new(
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
        ga.update_simulations_used(5);
        assert_eq!(ga.get_simulations_used(), 5);
    }

    #[test]
    fn test_budget_reached() {
        let mut ga = GeneticAlgorithm::new(
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
        assert_eq!(ga.budget_reached(), false);
        ga.update_simulations_used(100);
        assert_eq!(ga.budget_reached(), true);
    }

    #[test]
    fn test_mutate() {
        let ga = GeneticAlgorithm::new(
            mock_opti_function,
            2,   // Two individuals in population
            1.0, // 100% mutation rate for demonstration
            0.9,
            1.0,
            100,
            2,
            vec![0, 0],
            vec![10, 10],
        );

        let initial_population = vec![
            Arm::new(mock_opti_function, &vec![1, 1]),
            Arm::new(mock_opti_function, &vec![2, 2]),
        ];

        let mutated_population = ga.mutate(&initial_population);

        // Assuming the mutation is deterministic and in the expected bounds, you'd check like this:
        for (i, individual) in mutated_population.iter().enumerate() {
            let init_vector = initial_population[i].get_action_vector();
            let mut_vector = individual.get_action_vector();

            for j in 0..ga.dimension {
                assert!(mut_vector[j] >= ga.lower_bound[j]);
                assert!(mut_vector[j] <= ga.upper_bound[j]);
            }

            assert_ne!(mut_vector, init_vector); // since mutation rate is 100%
        }
    }

    #[test]
    fn test_crossover() {
        let ga = GeneticAlgorithm::new(
            mock_opti_function,
            2, // Two individuals for simplicity
            0.1,
            1.0, // 100% crossover rate for demonstration
            0.5,
            100,
            10, // higher dimension for demonstration so low probability of crossover leading to identical individuals
            vec![0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            vec![10, 10, 10, 10, 10, 10, 10, 10, 10, 10],
        );

        let crossover_population = ga.crossover();

        // Since the crossover rate is 100%, the two individuals should not be identical to the original individuals
        assert_ne!(
            crossover_population[0].get_action_vector(),
            ga.individuals[0].get_action_vector()
        );
        assert_ne!(
            crossover_population[1].get_action_vector(),
            ga.individuals[1].get_action_vector()
        );
    }
}
