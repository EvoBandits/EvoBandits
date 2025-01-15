from .gmab import Gmab
from sklearn.model_selection._search import BaseSearchCV
import numpy as np

def test_function(number: list) -> float:
    return sum([i ** 2 for i in number])

def tester():
    evaluation_budget = 10000

    bounds = [(-5, 10), (-5, 10)]
    gmaber = Gmab(test_function, bounds)

    print(gmaber.optimize(evaluation_budget))

# https://github.com/scikit-learn/scikit-learn/blob/main/sklearn/model_selection/_search.py#L433
# https://github.com/thuijskens/scikit-hyperband/blob/master/hyperband/search.py
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
    ):
        self.param_distributions = param_distributions
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

    def _run_search(self, evaluate_candidates):
        raise NotImplementedError
