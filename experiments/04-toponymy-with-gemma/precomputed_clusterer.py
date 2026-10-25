"""A Toponymy clusterer that carries the Clusterer's results instead of clustering.

`Toponymy.fit` skips its own clustering when its clusterer already has
`cluster_layers_` and `cluster_tree_` (toponymy 0.5.4, toponymy.py, the
`hasattr(self.clusterer, "cluster_layers_")` branch of `fit`). This class
builds both from the schema's cluster tree (`points.cluster` + `clusters`
rows) and makes `fit` / `fit_predict` raise, so any attempt to re-cluster is
loud rather than silent.
"""

from __future__ import annotations

import numpy as np
from toponymy.cluster_layer import ClusterLayerText
from toponymy.clustering import Clusterer, build_cluster_tree, centroids_from_labels
from toponymy.templates import PROMPT_TEMPLATES

from cluster_tree import layers_from_tree


class PrecomputedClusterer(Clusterer):
    def __init__(
        self,
        point_cluster: np.ndarray,
        clusters: list[dict],
        embedding_vectors: np.ndarray,
        layer_class=ClusterLayerText,
        **layer_kwargs,
    ):
        super().__init__()
        labels = layers_from_tree(point_cluster, clusters)
        # Toponymy.fit does not pass its prompt template to pre-fit layers, so
        # give them the default one, as ToponymyClusterer would via Toponymy.
        layer_kwargs.setdefault("prompt_template", PROMPT_TEMPLATES)
        layer_kwargs.setdefault("exemplar_delimiters", ['    * "', '"\n'])
        self.cluster_tree_ = build_cluster_tree(labels)
        self.cluster_layers_ = [
            layer_class(
                layer_labels,
                centroids_from_labels(layer_labels, embedding_vectors),
                layer_id=layer_id,
                **layer_kwargs,
            )
            for layer_id, layer_labels in enumerate(labels)
        ]

    def fit(self, *args, **kwargs):
        raise RuntimeError("PrecomputedClusterer holds precomputed clusters; it never clusters.")

    def fit_predict(self, *args, **kwargs):
        raise RuntimeError("PrecomputedClusterer holds precomputed clusters; it never clusters.")
