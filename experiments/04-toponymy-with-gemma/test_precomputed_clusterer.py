"""The Labeler hands Toponymy the Clusterer's results through a pre-fit clusterer."""

import numpy as np
import pytest
from toponymy.cluster_layer import ClusterLayerText
from toponymy.clustering import build_cluster_tree

from cluster_tree import tree_from_layers
from precomputed_clusterer import PrecomputedClusterer

LAYERS = [np.array([0, 0, 1, 1, 2, 2, -1, -1]), np.array([0, 0, 0, 0, 1, 1, 1, -1])]
# 2-d "embeddings": point i is at (i, 10 * i).
VECTORS = np.array([[i, 10 * i] for i in range(8)], dtype=np.float32)


@pytest.fixture
def clusterer():
    point_cluster, clusters = tree_from_layers(LAYERS)
    return PrecomputedClusterer(point_cluster, clusters, VECTORS)


def test_exposes_toponymy_cluster_layers_built_from_the_tree(clusterer):
    layers = clusterer.cluster_layers_
    assert all(isinstance(layer, ClusterLayerText) for layer in layers)
    assert [layer.layer_id for layer in layers] == [0, 1]
    assert [layer.cluster_labels.tolist() for layer in layers] == [x.tolist() for x in LAYERS]
    # Centroids are the mean embedding of each cluster's points.
    assert layers[1].centroid_vectors.tolist() == [[1.5, 15.0], [5.0, 50.0]]


def test_exposes_the_same_cluster_tree_toponymy_would_build(clusterer):
    assert clusterer.cluster_tree_ == build_cluster_tree(LAYERS)


def test_refuses_to_cluster_again(clusterer):
    with pytest.raises(RuntimeError, match="precomputed"):
        clusterer.fit(VECTORS, VECTORS)
    with pytest.raises(RuntimeError, match="precomputed"):
        clusterer.fit_predict(VECTORS, VECTORS)
