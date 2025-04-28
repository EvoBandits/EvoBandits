from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression

from evobandits import EvoBanditsSearchCV


if __name__ == "__main__":
    iris = load_iris()
    logistic = LogisticRegression(solver="saga", tol=1e-2, max_iter=200, random_state=0)
    distributions = {
        "max_iter": (100, 200),
        "random_state": (0, 100),
    }
    clf = EvoBanditsSearchCV(logistic, distributions)
    search = clf.fit(iris.data, iris.target)
    print(search.best_params_)
