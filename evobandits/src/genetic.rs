use std::collections::HashSet;

use rand::rngs::StdRng;
use rand::{Rng, SeedableRng};
use rand_distr::{Distribution, Normal};

use crate::arm::Arm;

pub const POPULATION_SIZE_DEFAULT: usize = 20;
pub const MUTATION_RATE_DEFAULT: f64 = 0.25;
pub const CROSSOVER_RATE_DEFAULT: f64 = 1.0;
pub const MUTATION_SPAN_DEFAULT: f64 = 0.1;

pub struct GeneticAlgorithm {
    pub mutation_rate: f64,
    pub crossover_rate: f64,
    pub mutation_span: f64,
    pub population_size: usize,
    pub dimension: usize,
    pub lower_bound: Vec<i32>,
    pub upper_bound: Vec<i32>,
}

impl GeneticAlgorithm {
    pub fn set_bounds(&mut self, bounds: Vec<(i32, i32)>) {
        self.dimension = bounds.len();
        self.lower_bound = bounds.iter().map(|&(low, _)| low).collect::<Vec<i32>>();
        self.upper_bound = bounds.iter().map(|&(_, high)| high).collect::<Vec<i32>>();
    }

    pub fn validate(&self) {
        if self.population_size == 0 {
            panic!("population_size cannot be 0");
        }
        if !(0.0..=1.0).contains(&self.mutation_rate) {
            panic!("mutation_rate must be between 0.0 and 1.0");
        }
        if !(0.0..=1.0).contains(&self.crossover_rate) {
            panic!("crossover_rate must be between 0.0 and 1.0");
        }
        if !(0.0..=1.0).contains(&self.mutation_span) {
            panic!("mutation_span must be between 0.0 and 1.0");
        }

        // Raise an Exception if population_size > solution space
        let mut solution_size: usize = 1;
        let mut not_enough_solutions = true;
        for i in 0..self.dimension {
            solution_size *= (self.upper_bound[i] - self.lower_bound[i] + 1) as usize;
            if solution_size >= self.population_size {
                not_enough_solutions = false;
                break;
            }
        }
        if not_enough_solutions {
            panic!(
                "population_size ({}) is larger than the number of potential solutions ({}).",
                self.population_size, solution_size
            );
        }
    }

    pub(crate) fn generate_new_population(&self, seed: u64) -> Vec<Arm> {
        let mut individuals: Vec<Arm> = Vec::new();
        let mut rng: StdRng = SeedableRng::seed_from_u64(seed);

        while individuals.len() < self.population_size {
            let candidate_solution: Vec<i32> = (0..self.dimension)
                .map(|j| rng.random_range(self.lower_bound[j]..=self.upper_bound[j]))
                .collect();

            let candidate_arm = Arm::new(&candidate_solution);

            if !individuals.contains(&candidate_arm) {
                individuals.push(candidate_arm);
            }
        }
        individuals
    }

    pub(crate) fn crossover(&self, seed: u64, population: &[Arm]) -> Vec<Arm> {
        let mut crossover_pop: Vec<Arm> = Vec::new();
        let population_size = self.population_size;
        let mut rng: StdRng = SeedableRng::seed_from_u64(seed);

        let step = 2;
        for i in (0..population_size - (population_size % step)).step_by(step) {
            if rng.random::<f64>() < self.crossover_rate && self.dimension > 1 {
                // Crossover
                let max_dim_index = self.dimension - 1;
                let swap_rv = rng.random_range(1..=max_dim_index);

                for j in 1..=max_dim_index {
                    if swap_rv == j {
                        let mut cross_vec_1: Vec<i32> =
                            population[i].get_action_vector()[0..j].to_vec();
                        cross_vec_1.extend_from_slice(
                            &population[i + 1].get_action_vector()[j..=max_dim_index],
                        );

                        let mut cross_vec_2: Vec<i32> =
                            population[i + 1].get_action_vector()[0..j].to_vec();
                        cross_vec_2.extend_from_slice(
                            &population[i].get_action_vector()[j..=max_dim_index],
                        );

                        let new_individual_1 = Arm::new(&cross_vec_1);
                        let new_individual_2 = Arm::new(&cross_vec_2);

                        crossover_pop.push(new_individual_1);
                        crossover_pop.push(new_individual_2);
                    }
                }
            } else {
                // No Crossover
                crossover_pop.push(population[i].clone());
                crossover_pop.push(population[i + 1].clone());
            }
        }

        crossover_pop
    }

    pub(crate) fn mutate(&self, seed: u64, population: &[Arm]) -> Vec<Arm> {
        let mut mutated_population = Vec::new();
        let mut seen = HashSet::new();
        let mut rng = StdRng::seed_from_u64(seed);

        for individual in population.iter() {
            // Clone the action vector
            let mut new_action_vector = individual.get_action_vector().to_vec(); // Here I assumed `get_action_vector` returns a slice or Vec

            for (i, value) in new_action_vector.iter_mut().enumerate() {
                if rng.random::<f64>() < self.mutation_rate {
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

            let new_individual = Arm::new(new_action_vector.as_slice());

            if seen.insert(new_individual.clone()) {
                mutated_population.push(new_individual);
            }
        }

        mutated_population
    }
}

impl Default for GeneticAlgorithm {
    fn default() -> Self {
        GeneticAlgorithm {
            mutation_rate: MUTATION_RATE_DEFAULT,
            crossover_rate: CROSSOVER_RATE_DEFAULT,
            mutation_span: MUTATION_SPAN_DEFAULT,
            population_size: POPULATION_SIZE_DEFAULT,
            dimension: 1,
            lower_bound: vec![0],
            upper_bound: vec![1],
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    // Valid inputs that mark (some of) the edge cases for the parameters
    const POPULATION_SIZE: usize = 1;
    const MUTATION_RATE: f64 = 1.0;
    const CROSSOVER_RATE: f64 = 0.0;
    const MUTATION_SPAN: f64 = 0.0;
    const SEED: u64 = 42;

    #[test]
    fn test_ga_default_config() {
        let ga = GeneticAlgorithm::default();

        assert_eq!(ga.population_size, POPULATION_SIZE_DEFAULT);
        assert_eq!(ga.mutation_rate, MUTATION_RATE_DEFAULT);
        assert_eq!(ga.crossover_rate, CROSSOVER_RATE_DEFAULT);
        assert_eq!(ga.mutation_span, MUTATION_SPAN_DEFAULT);
    }

    #[test]
    fn test_ga_modified_default_config() {
        let ga = GeneticAlgorithm {
            population_size: POPULATION_SIZE,
            ..Default::default()
        };
        ga.validate();

        assert_eq!(ga.population_size, POPULATION_SIZE);
        assert_eq!(ga.mutation_rate, MUTATION_RATE_DEFAULT);
        assert_eq!(ga.crossover_rate, CROSSOVER_RATE_DEFAULT);
        assert_eq!(ga.mutation_span, MUTATION_SPAN_DEFAULT);
    }

    #[test]
    fn test_ga_all_modified_config() {
        let ga = GeneticAlgorithm {
            population_size: POPULATION_SIZE,
            mutation_rate: MUTATION_RATE,
            crossover_rate: CROSSOVER_RATE,
            mutation_span: MUTATION_SPAN,
            dimension: 1,
            lower_bound: vec![0],
            upper_bound: vec![1],
        };
        ga.validate();

        assert_eq!(ga.population_size, POPULATION_SIZE);
        assert_eq!(ga.mutation_rate, MUTATION_RATE);
        assert_eq!(ga.crossover_rate, CROSSOVER_RATE);
        assert_eq!(ga.mutation_span, MUTATION_SPAN);
    }

    #[test]
    #[should_panic(expected = "population_size")]
    fn test_invalid_population_size() {
        let ga = GeneticAlgorithm {
            population_size: 0,
            ..Default::default()
        };
        ga.validate();
    }

    #[test]
    #[should_panic(expected = "mutation_rate")]
    fn test_invalid_large_mutation_rate() {
        let ga = GeneticAlgorithm {
            mutation_rate: 1.01,
            ..Default::default()
        };
        ga.validate();
    }

    #[test]
    #[should_panic(expected = "mutation_rate")]
    fn test_invalid_small_mutation_rate() {
        let ga = GeneticAlgorithm {
            mutation_rate: -0.01,
            ..Default::default()
        };
        ga.validate();
    }

    #[test]
    #[should_panic(expected = "crossover_rate")]
    fn test_invalid_large_crossover_rate() {
        let ga = GeneticAlgorithm {
            crossover_rate: 1.01,
            ..Default::default()
        };
        ga.validate();
    }

    #[test]
    #[should_panic(expected = "crossover_rate")]
    fn test_invalid_small_crossover_rate() {
        let ga = GeneticAlgorithm {
            crossover_rate: -0.01,
            ..Default::default()
        };
        ga.validate();
    }

    #[test]
    #[should_panic(expected = "mutation_span")]
    fn test_invalid_large_mutation_span() {
        let ga = GeneticAlgorithm {
            mutation_span: 1.01,
            ..Default::default()
        };
        ga.validate();
    }

    #[test]
    #[should_panic(expected = "mutation_span")]
    fn test_invalid_small_mutation_span() {
        let ga = GeneticAlgorithm {
            mutation_span: -0.01,
            ..Default::default()
        };
        ga.validate();
    }

    #[test]
    #[should_panic(expected = "number of potential solutions")]
    fn test_invalid_bounds() {
        // initialize a ga with less solutions than population size
        let ga = GeneticAlgorithm {
            population_size: 20,
            dimension: 2,
            lower_bound: vec![0, 0],
            upper_bound: vec![1, 1],
            ..Default::default()
        };
        ga.validate();
    }

    #[test]
    fn test_get_population_size() {
        let ga = GeneticAlgorithm {
            population_size: 10,
            mutation_rate: 0.1,
            crossover_rate: 0.9,
            mutation_span: 0.5,
            dimension: 2,
            lower_bound: vec![0, 0],
            upper_bound: vec![10, 10],
        };
        assert_eq!(ga.population_size, 10);
    }

    #[test]
    fn test_mutate() {
        let ga = GeneticAlgorithm {
            population_size: 2, // Two individuals in population
            mutation_rate: 1.0, // 100% mutation rate for demonstration
            crossover_rate: 0.9,
            mutation_span: 1.0,
            dimension: 2,
            lower_bound: vec![0, 0],
            upper_bound: vec![10, 10],
        };

        let initial_population = vec![Arm::new(&vec![1, 1]), Arm::new(&vec![2, 2])];

        let mutated_population = ga.mutate(SEED, &initial_population);

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
        let ga = GeneticAlgorithm {
            population_size: 2, // Two individuals for simplicity
            mutation_rate: 0.1,
            crossover_rate: 1.0, // 100% crossover rate for demonstration
            mutation_span: 0.5,
            dimension: 10, // higher dimension for demonstration so low probability of crossover leading to identical individuals
            lower_bound: vec![0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            upper_bound: vec![10, 10, 10, 10, 10, 10, 10, 10, 10, 10],
        };

        let initial_population = vec![
            Arm::new(&vec![0, 1, 2, 3, 4, 5, 6, 7, 8, 9]),
            Arm::new(&vec![9, 8, 7, 6, 5, 4, 3, 2, 1, 0]),
        ];

        let crossover_population = ga.crossover(SEED, &initial_population);

        // Since the crossover rate is 100%, the two individuals should not be identical to the original individuals
        assert_ne!(
            crossover_population[0].get_action_vector(),
            initial_population[0].get_action_vector()
        );
        assert_ne!(
            crossover_population[1].get_action_vector(),
            initial_population[1].get_action_vector()
        );
    }

    #[test]
    fn test_crossover_dimension_1() {
        let ga = GeneticAlgorithm {
            population_size: 2, // Two individuals for simplicity
            mutation_rate: 0.1,
            crossover_rate: 1.0, // 100% crossover rate for demonstration
            mutation_span: 0.5,
            dimension: 1, // Using dimension 1
            lower_bound: vec![0],
            upper_bound: vec![10],
        };

        let initial_population = vec![Arm::new(&vec![3]), Arm::new(&vec![7])];

        // This should not panic
        let crossover_population = ga.crossover(SEED, &initial_population);

        // Verify we have the expected number of individuals
        assert_eq!(crossover_population.len(), 2);

        // With dimension 1, crossover should just clone the individuals
        assert_eq!(
            crossover_population[0].get_action_vector(),
            initial_population[0].get_action_vector()
        );
        assert_eq!(
            crossover_population[1].get_action_vector(),
            initial_population[1].get_action_vector()
        );
    }

    #[test]
    fn test_reproduction_with_seeding() {
        // Helper function that generates and modifies a population using a seed.
        fn generate_population(seed: u64) -> Vec<Arm> {
            let ga = GeneticAlgorithm {
                population_size: 10,
                mutation_rate: 0.1,
                crossover_rate: 0.9,
                mutation_span: 1.0,
                dimension: 2,
                lower_bound: vec![0, 0],
                upper_bound: vec![10, 10],
            };

            let mut population = ga.generate_new_population(seed);
            population = ga.crossover(seed, &population);
            population = ga.mutate(seed, &population);

            return population;
        }

        // The same seed should lead to the same population
        assert_eq!(generate_population(SEED), generate_population(SEED));

        // A different seed should not lead to the same population
        assert_ne!(generate_population(SEED), generate_population(SEED + 1));
    }
}
