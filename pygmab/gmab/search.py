from .gmab import Gmab
from sklearn.model_selection._search import BaseSearchCV
import numpy as np

# https://github.com/scikit-learn/scikit-learn/blob/main/sklearn/model_selection/_search.py#L433
class GmabSearchCV(BaseSearchCV):
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
        gmab_iterations=50,
    ):
        """
        param_distributions: dict
            Dictionary of parameter_name -> (lower_bound, upper_bound),
            all of which must be integer bounds.
        gmab_iterations: int
            How many iterations (simulation budget) Gmab should run internally.
        """
        self.param_distributions = param_distributions
        self.gmab_iterations = gmab_iterations

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
        3) Invokes Gmab to search for the best hyperparameters.
        4) Finally, calls evaluate_candidates one last time with the best found
           parameters so they are recorded by scikit-learn.
        """

        # 1) Collect parameter names and integer bounds
        #    Example: param_distributions = {"x": (-5, 10), "y": (0, 5)}
        #    We will map these onto a list-like domain as Gmab expects.
        param_names = list(self.param_distributions.keys())
        bounds = [self.param_distributions[name] for name in param_names]

        # 2) Define the Python objective function for Gmab
        #    action_vector is a list of i32 from Rust's perspective
        #    We call scikit-learn's evaluate_candidates([param_dict]) to get scores,
        #    and return that cross-validation mean_test_score so that Gmab can
        #    attempt to maximize it.
        def gmab_objective(action_vector: list) -> float:
            # Build param_dict from the action vector
            param_dict = {}
            for i, name in enumerate(param_names):
                param_dict[name] = action_vector[i]

            results = evaluate_candidates([param_dict])
            mean_score = results.get("mean_test_score", np.nan)[0]
            self._latest_score = mean_score
            # gmab minimizes the objective, so we negate the score
            return mean_score * -1

        # 3) Create the Gmab optimizer and search for the best param configuration
        gmab_opt = Gmab(gmab_objective, bounds)
        best_action_vector = gmab_opt.optimize(self.gmab_iterations)

        # 4) Evaluate the best param set again (so scikit-learn knows about it)
        best_dict = {}
        for i, name in enumerate(param_names):
            best_dict[name] = best_action_vector[i]
        evaluate_candidates([best_dict])
