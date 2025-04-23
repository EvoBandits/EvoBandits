// Default values for the GMAB Algortihm
pub const POPULATION_SIZE_DEFAULT: usize = 20;
pub const MUTATION_RATE_DEFAULT: f64 = 0.25;
pub const CROSSOVER_RATE_DEFAULT: f64 = 1.0;
pub const MUTATION_SPAN_DEFAULT: f64 = 0.1;

pub struct GmabOptions {
    pub population_size: usize,
    pub mutation_rate: f64,
    pub crossover_rate: f64,
    pub mutation_span: f64,
}

impl GmabOptions {
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
        if self.mutation_span < 0.0 {
            panic!("mutation_span must be 0.0 or greater");
        }
    }
}

impl Default for GmabOptions {
    fn default() -> Self {
        GmabOptions {
            population_size: POPULATION_SIZE_DEFAULT,
            mutation_rate: MUTATION_RATE_DEFAULT,
            crossover_rate: CROSSOVER_RATE_DEFAULT,
            mutation_span: MUTATION_SPAN_DEFAULT,
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    // Valid inputs that mark (some of) the edge cases for the paramters
    const POPULATION_SIZE: usize = 1;
    const MUTATION_RATE: f64 = 1.0;
    const CROSSOVER_RATE: f64 = 0.0;
    const MUTATION_SPAN: f64 = 1.1;

    #[test]
    fn test_default() {
        let options = GmabOptions::default();
        options.validate();

        assert_eq!(options.population_size, POPULATION_SIZE_DEFAULT);
        assert_eq!(options.mutation_rate, MUTATION_RATE_DEFAULT);
        assert_eq!(options.crossover_rate, CROSSOVER_RATE_DEFAULT);
        assert_eq!(options.mutation_span, MUTATION_SPAN_DEFAULT);
    }

    #[test]
    fn test_default_with_modification() {
        let options = GmabOptions {
            population_size: POPULATION_SIZE,
            ..Default::default()
        };
        options.validate();

        assert_eq!(options.population_size, POPULATION_SIZE);
        assert_eq!(options.mutation_rate, MUTATION_RATE_DEFAULT);
        assert_eq!(options.crossover_rate, CROSSOVER_RATE_DEFAULT);
        assert_eq!(options.mutation_span, MUTATION_SPAN_DEFAULT);
    }

    #[test]
    fn test_only_modification() {
        let options = GmabOptions {
            population_size: POPULATION_SIZE,
            mutation_rate: MUTATION_RATE,
            crossover_rate: CROSSOVER_RATE,
            mutation_span: MUTATION_SPAN,
        };
        options.validate();

        assert_eq!(options.population_size, POPULATION_SIZE);
        assert_eq!(options.mutation_rate, MUTATION_RATE);
        assert_eq!(options.crossover_rate, CROSSOVER_RATE);
        assert_eq!(options.mutation_span, MUTATION_SPAN);
    }

    #[test]
    #[should_panic(expected = "population_size")]
    fn test_invalid_population_size() {
        let options = GmabOptions {
            population_size: 0,
            ..Default::default()
        };
        options.validate();
    }

    #[test]
    #[should_panic(expected = "mutation_rate")]
    fn test_invalid_large_mutation_rate() {
        let options = GmabOptions {
            mutation_rate: 1.01,
            ..Default::default()
        };
        options.validate();
    }

    #[test]
    #[should_panic(expected = "mutation_rate")]
    fn test_invalid_small_mutation_rate() {
        let options = GmabOptions {
            mutation_rate: -0.01,
            ..Default::default()
        };
        options.validate();
    }

    #[test]
    #[should_panic(expected = "crossover_rate")]
    fn test_invalid_large_crossover_rate() {
        let options = GmabOptions {
            crossover_rate: 1.01,
            ..Default::default()
        };
        options.validate();
    }

    #[test]
    #[should_panic(expected = "crossover_rate")]
    fn test_invalid_small_crossover_rate() {
        let options = GmabOptions {
            crossover_rate: -0.01,
            ..Default::default()
        };
        options.validate();
    }

    #[test]
    // ToDo: Check if this should really be allowed.
    // #[should_panic(expected = "mutation_span")]
    fn test_invalid_large_mutation_span() {
        let options = GmabOptions {
            mutation_span: 1.01,
            ..Default::default()
        };
        options.validate();
    }

    #[test]
    #[should_panic(expected = "mutation_span")]
    fn test_invalid_small_mutation_span() {
        let options = GmabOptions {
            mutation_span: -0.01,
            ..Default::default()
        };
        options.validate();
    }
}
