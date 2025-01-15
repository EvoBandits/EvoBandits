from .gmab import Gmab
from sklearn.model_selection._search import BaseSearchCV

def test_function(number: list) -> float:
    return sum([i ** 2 for i in number])

def tester():
    evaluation_budget = 10000

    bounds = [(-5, 10), (-5, 10)]
    gmaber = Gmab(test_function, bounds)

    print(gmaber.optimize(evaluation_budget))
