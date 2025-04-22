use rand::RngCore;

pub struct GmabOptions {
    pub population_size: usize,
    pub mutation_rate: f64,
    pub crossover_rate: f64,
    pub mutation_span: f64,
    pub seed: u64,
}

// Default values for the Genetic algorithm
impl GmabOptions {
    pub const POPULATION_SIZE_DEFAULT: usize = 20;
    pub const MUTATION_RATE_DEFAULT: f64 = 0.25;
    pub const CROSSOVER_RATE_DEFAULT: f64 = 1.0;
    pub const MUTATION_SPAN_DEFAULT: f64 = 0.1;

    pub fn validate(&self) {
        if self.population_size == 0 {
            panic!("population_size cannot be 0");
        }
        if self.mutation_rate < 0.0 || self.mutation_rate > 1.0 {
            panic!("mutation_rate must be between 0.0 and 1.0");
        }
        if self.crossover_rate < 0.0 || self.crossover_rate > 1.0 {
            panic!("crossover_rate must be between 0.0 and 1.0");
        }
        if self.mutation_span < 0.0 {
            panic!("mutation_span must be 0.0 or greater");
        }
    }
}

impl Default for GmabOptions {
    fn default() -> Self {
        GmabOptions {
            population_size: Self::POPULATION_SIZE_DEFAULT,
            mutation_rate: Self::MUTATION_RATE_DEFAULT,
            crossover_rate: Self::CROSSOVER_RATE_DEFAULT,
            mutation_span: Self::MUTATION_SPAN_DEFAULT,
            seed: rand::rng().next_u64(), // No default, fall back to system entropy instead
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_default() {
        let options = GmabOptions::default();

        assert_eq!(options.population_size, 20);
        assert_eq!(options.mutation_rate, 0.25);
        assert_eq!(options.crossover_rate, 1.0);
        assert_eq!(options.mutation_span, 0.1);
        let _: u64 = options.seed; // Will fail to compile if seed is not u64
    }

    #[test]
    #[should_panic(expected = "population_size")]
    fn test_population_size_not_zero() {
        let options = GmabOptions {
            population_size: 0,
            ..Default::default()
        };
        options.validate();
    }

    #[test]
    #[should_panic(expected = "mutation_rate")]
    fn test_mutation_rate_too_small() {
        let options = GmabOptions {
            mutation_rate: -0.01,
            ..Default::default()
        };
        options.validate();
    }

    #[test]
    #[should_panic(expected = "mutation_rate")]
    fn test_mutation_rate_too_large() {
        let options = GmabOptions {
            mutation_rate: 1.01,
            ..Default::default()
        };
        options.validate();
    }

    #[test]
    #[should_panic(expected = "crossover_rate")]
    fn test_crossover_rate_too_small() {
        let options = GmabOptions {
            crossover_rate: -0.01,
            ..Default::default()
        };
        options.validate();
    }

    #[test]
    #[should_panic(expected = "crossover_rate")]
    fn test_crossover_rate_too_large() {
        let options = GmabOptions {
            crossover_rate: 1.01,
            ..Default::default()
        };
        options.validate();
    }

    #[test]
    #[should_panic(expected = "mutation_span")]
    fn test_mutation_span_too_small() {
        let options = GmabOptions {
            mutation_span: -0.01,
            ..Default::default()
        };
        options.validate();
    }
}
