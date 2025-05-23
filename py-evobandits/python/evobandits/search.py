# Copyright 2025 EvoBandits
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import numpy as np
from sklearn.model_selection._search import BaseSearchCV

from evobandits.evobandits import EvoBandits


# https://github.com/scikit-learn/scikit-learn/blob/main/sklearn/model_selection/_search.py#L433
class EvoBanditsSearchCV(BaseSearchCV):
    def __init__(
        self,
        estimator,
        param_distributions,
        *,
        scoring=None,
        n_jobs=None,
        refit=True,
        cv=None,
        verbose=0,
        pre_dispatch="2*n_jobs",
        error_score=np.nan,
        return_train_score=True,
        n_trials=50,
    ):
        """
        param_distributions: dict
            Dictionary of parameter_name -> (lower_bound, upper_bound),
            all of which must be integer bounds.
        n_trials: int
            How many trials (simulation budget) EvoBandits should run internally.
        """
        self.param_distributions = param_distributions
        self.n_trials = n_trials

        super().__init__(
            estimator=estimator,
            scoring=scoring,
            n_jobs=n_jobs,
            refit=refit,
            cv=cv,
            verbose=verbose,
            pre_dispatch=pre_dispatch,
            error_score=error_score,
            return_train_score=return_train_score,
        )

        # A place to stash the last known score from evaluate_candidates
        self._latest_score = None

    def _run_search(self, evaluate_candidates):
        """
        Overridden method from BaseSearchCV:
        1) Builds an integer-bounded search space from self.param_distributions.
        2) Defines a Python function that calls evaluate_candidates to retrieve
           cross-validation scores.
        3) Invokes EvoBandits to search for the best hyperparameters.
        4) Finally, calls evaluate_candidates one last time with the best found
           parameters so they are recorded by scikit-learn.
        """

        # 1) Collect parameter names and integer bounds
        #    Example: param_distributions = {"x": (-5, 10), "y": (0, 5)}
        #    We will map these onto a list-like domain as EvoBandits expects.
        param_names = list(self.param_distributions.keys())
        bounds = [self.param_distributions[name] for name in param_names]

        # 2) Define the Python objective function for EvoBandits
        #    action_vector is a list of i32 from Rust's perspective
        #    We call scikit-learn's evaluate_candidates([param_dict]) to get scores,
        #    and return that cross-validation mean_test_score so that EvoBandits can
        #    attempt to maximize it.
        def evobandits_objective(action_vector: list) -> float:
            # Build param_dict from the action vector
            param_dict = {}
            for i, name in enumerate(param_names):
                param_dict[name] = action_vector[i]

            results = evaluate_candidates([param_dict])
            mean_score = results.get("mean_test_score", np.nan)[0]
            self._latest_score = mean_score
            # evobandits minimizes the objective, so we negate the score
            return mean_score * -1

        # 3) Create the EvoBandits optimizer and search for the best param configuration
        evobandits_opt = EvoBandits()
        best_arms = evobandits_opt.optimize(
          evobandits_objective, bounds, self.n_trials, n_best=1
        )
        best_action_vector = best_arms[0].to_dict.get("action_vector")

        # 4) Evaluate the best param set again (so scikit-learn knows about it)
        best_dict = {}
        for i, name in enumerate(param_names):
            best_dict[name] = best_action_vector[i]
        evaluate_candidates([best_dict])
