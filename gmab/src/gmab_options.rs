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
    pub fn new() -> GmabOptions {
        GmabOptions {
            population_size: POPULATION_SIZE_DEFAULT,
            mutation_rate: MUTATION_RATE_DEFAULT,
            crossover_rate: CROSSOVER_RATE_DEFAULT,
            mutation_span: MUTATION_SPAN_DEFAULT,
        }
    }

    //
    // pub fn validate(&self) {
    //    if self.population_size == 0 {
    //        panic!("population_size cannot be 0");
    //    }
    //    if !(0.0..=1.0).contains(&self.mutation_rate) {
    //        panic!("mutation_rate must be between 0.0 and 1.0");
    //    }
    //    if !(0.0..=1.0).contains(&self.crossover_rate) {
    //        panic!("crossover_rate must be between 0.0 and 1.0");
    //    }
    //    if self.mutation_span < 0.0 {
    //        panic!("mutation_span must be 0.0 or greater");
    //     }
    // }

    pub fn with_population_size(mut self, population_size: usize) -> GmabOptions {
        self.population_size = population_size;
        // self.validate();
        self
    }

    pub fn with_mutation_rate(mut self, mutation_rate: f64) -> GmabOptions {
        self.mutation_rate = mutation_rate;
        self
    }

    pub fn with_crossover_rate(mut self, crossover_rate: f64) -> GmabOptions {
        self.crossover_rate = crossover_rate;
        self
    }

    pub fn with_mutation_span(mut self, mutation_span: f64) -> GmabOptions {
        self.mutation_span = mutation_span;
        self
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_defaults() {
        let options = GmabOptions::new();

        assert_eq!(options.population_size, 20);
        assert_eq!(options.mutation_rate, 0.25);
        assert_eq!(options.crossover_rate, 1.0);
        assert_eq!(options.mutation_span, 0.1);
    }

    #[test]
    fn test_with_modification() {
        let population_size = 10;
        let mutation_rate = 0.5;
        let crossover_rate = 0.5;
        let mutation_span = 1.1;

        let options = GmabOptions::new()
            .with_population_size(population_size)
            .with_mutation_rate(mutation_rate)
            .with_crossover_rate(crossover_rate)
            .with_mutation_span(mutation_span);

        assert_eq!(options.population_size, population_size);
        assert_eq!(options.mutation_rate, mutation_rate);
        assert_eq!(options.crossover_rate, crossover_rate);
        assert_eq!(options.mutation_span, mutation_span);
    }

    //
    //#[test]
    // #[should_panic(expected = "population_size")]
    // fn test_population_size_not_zero() {
    //    GmabOptions::new().with_population_size(0);
    // }
    //
    // ToDo: Find a fix and Do not merge before the bypass issue is fixed
    // Or can this be accepted (Gmab uses one state of the options.)
    // #[test]
    // #[should_panic(expected = "population_size")]
    // fn test_population_size_bypass() {
    //    let mut options = GmabOptions::new();
    //    options.population_size = 0;
    // }
}
