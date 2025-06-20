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

use criterion::{criterion_group, criterion_main, BenchmarkId, Criterion};
use evobandits::evobandits::GMAB;
use rand::rng;
use rand_distr::{Distribution, Normal};
use std::hint::black_box;

pub fn noisy_rosenbrock(x: &[i32]) -> f64 {
    let x_f64 = x[0] as f64 / 10.0;
    let y_f64 = x[1] as f64 / 10.0;

    // Rosenbrock function
    let term1 = (1.0 - x_f64).powi(2);
    let term2 = 100.0 * (y_f64 - x_f64.powi(2)).powi(2);
    let base_value = term1 + term2;

    // Add Gaussian noise
    let mut rng = rng();
    let normal = Normal::new(0.0, 5.0).unwrap();
    let noise = normal.sample(&mut rng);

    base_value + noise
}

fn benchmark_evobandits(c: &mut Criterion) {
    let mut group = c.benchmark_group("Rosenbrock Optimization");

    group.measurement_time(std::time::Duration::from_secs(60));

    // Simulate different budgets
    for n_trials in [10_000, 100_000].iter() {
        group.bench_with_input(
            BenchmarkId::new("Noisy", n_trials),
            n_trials,
            |b, &n_trials| {
                b.iter(|| {
                    let mut gmab = GMAB::new(Default::default());
                    let bounds = vec![(-50, 50), (-50, 50)];

                    // Run the optimization
                    let result = gmab.optimize(
                        black_box(noisy_rosenbrock),
                        black_box(bounds),
                        black_box(n_trials),
                        1,
                        Default::default(),
                    );

                    result
                });
            },
        );
    }

    group.finish();
}

criterion_group!(benches, benchmark_evobandits);
criterion_main!(benches);
