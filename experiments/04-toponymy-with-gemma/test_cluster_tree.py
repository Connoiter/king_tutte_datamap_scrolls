"""Cluster layers <-> the schema's cluster tree (parent pointers).

The schema stores `points.cluster` (the finest cluster a point is in, or -1)
and one `clusters` row per cluster with its `layer` and `parent`. The
Clusterer turns Toponymy's per-layer label arrays into that shape; the
Labeler turns it back into per-layer arrays for Toponymy.
"""

import numpy as np

from cluster_tree import layers_from_tree, tree_from_layers

# Worked example: 8 points, two layers.
#   layer 0 (finest): clusters 0, 1, 2; points 6 and 7 are noise.
#   layer 1:          clusters 0 = {0..3}, 1 = {4, 5, 6}; point 7 is noise.
LAYER_0 = np.array([0, 0, 1, 1, 2, 2, -1, -1])
LAYER_1 = np.array([0, 0, 0, 0, 1, 1, 1, -1])


def test_clusters_get_ids_unique_across_layers_and_parents_in_the_coarser_layer():
    _, clusters = tree_from_layers([LAYER_0, LAYER_1])
    assert clusters == [
        {"cluster": 0, "layer": 0, "parent": 3},
        {"cluster": 1, "layer": 0, "parent": 3},
        {"cluster": 2, "layer": 0, "parent": 4},
        {"cluster": 3, "layer": 1, "parent": None},
        {"cluster": 4, "layer": 1, "parent": None},
    ]


def test_each_point_gets_its_finest_cluster_or_minus_one():
    point_cluster, _ = tree_from_layers([LAYER_0, LAYER_1])
    # Point 6 is noise at layer 0 but in layer-1 cluster 1 (id 4).
    assert point_cluster.tolist() == [0, 0, 1, 1, 2, 2, 4, -1]


def test_layers_are_rebuilt_from_the_tree():
    point_cluster, clusters = tree_from_layers([LAYER_0, LAYER_1])
    rebuilt = layers_from_tree(point_cluster, clusters)
    assert [layer.tolist() for layer in rebuilt] == [LAYER_0.tolist(), LAYER_1.tolist()]


def test_a_parent_can_skip_a_layer_where_the_cluster_is_noise():
    # Layer-0 cluster 1 (points 2, 3) is noise at layer 1 but inside the single
    # layer-2 cluster. Its parent is that layer-2 cluster (id 3).
    layers = [
        np.array([0, 0, 1, 1]),
        np.array([0, 0, -1, -1]),
        np.array([0, 0, 0, 0]),
    ]
    point_cluster, clusters = tree_from_layers(layers)
    assert {row["cluster"]: row["parent"] for row in clusters} == {0: 2, 1: 3, 2: 3, 3: None}
    rebuilt = layers_from_tree(point_cluster, clusters)
    assert [layer.tolist() for layer in rebuilt] == [layer.tolist() for layer in layers]
