"""
Objective function and useful parameters for a clustering problem,
which serves as an example to demonstrate the use of various parameters types.

The test example is based on an example from sklearn:
Title: Comparison of the K-Means and MiniBatchKMeans clustering algorithms
Source: https://scikit-learn.org/stable/auto_examples/cluster/plot_mini_batch_kmeans.html#sphx-glr-auto-examples-cluster-plot-mini-batch-kmeans-py
Last accessed: 2025-04-18
Version: 1.6.1
"""

import numpy as np
from evobandits import CategoricalParam, FloatParam, IntParam
from sklearn.cluster import KMeans, MiniBatchKMeans
from sklearn.datasets import make_blobs

# Useful parameters
PARAMS = {
    "algorithm": CategoricalParam([KMeans, MiniBatchKMeans]),
    "init": CategoricalParam(["k-means++", "random"]),
    "n_clusters": IntParam(1, 10),
    "tol": FloatParam(1e-4, 1e-2),
}
BOUNDS = [(0, 1), (0, 1), (1, 10), (0, 100)]


# Generate sample data
np.random.seed(0)

_centers = [[1, 1], [-1, -1], [1, -1]]
_n_clusters = len(_centers)
_X, labels_true = make_blobs(n_samples=10000, centers=_centers, cluster_std=0.7)


def function(algorithm, init, n_clusters, tol) -> float:
    """Evaluate the inertia of the clustering that results from the given parameters."""
    clusterer = algorithm(init=init, n_clusters=n_clusters, tol=tol, n_init=10)
    clusterer.fit(_X)
    return clusterer.inertia_


if __name__ == "__main__":
    # Example usage
    result = function(KMeans, "k-means++", 3, 0.001)
    print(f"Clustering inertia: {result}")
