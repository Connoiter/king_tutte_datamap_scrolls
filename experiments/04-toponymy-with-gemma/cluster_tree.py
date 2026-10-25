"""Convert between per-layer cluster label arrays and the schema's cluster tree.

Per-layer arrays are what Toponymy (and DataMapPlot) use: one int array per
cluster layer, layer 0 finest, with local cluster labels 0..k-1 and -1 for
noise. The datamap schema instead stores:

- `points.cluster`: the finest cluster a point belongs to, or -1 if it is noise
  at every layer;
- one `clusters` row per cluster: `cluster` (unique across layers), `layer`,
  and `parent`, the cluster in the nearest coarser layer that contains it
  (None at the top). Toponymy's own tree builder also lets a parent skip a
  layer when the cluster is noise in the layer just above.

Global ids are assigned layer by layer: layer 0's clusters first, in local
label order, then layer 1's, and so on.
"""

from __future__ import annotations

import numpy as np


def _offsets(layers: list[np.ndarray]) -> list[int]:
    offsets, total = [], 0
    for labels in layers:
        offsets.append(total)
        total += int(labels.max()) + 1
    return offsets


def tree_from_layers(layers: list[np.ndarray]) -> tuple[np.ndarray, list[dict]]:
    """Per-layer label arrays -> (points.cluster, clusters rows)."""
    layers = [np.asarray(labels) for labels in layers]
    offsets = _offsets(layers)

    point_cluster = np.full(layers[0].shape[0], -1, dtype=np.int64)
    for layer_index in range(len(layers) - 1, -1, -1):  # coarse to fine
        labels = layers[layer_index]
        member = labels >= 0
        point_cluster[member] = labels[member] + offsets[layer_index]

    clusters = []
    for layer_index, labels in enumerate(layers):
        for local in range(int(labels.max()) + 1):
            members = labels == local
            parent = None
            for coarser in range(layer_index + 1, len(layers)):
                above = layers[coarser][members]
                above = above[above >= 0]
                if above.size:
                    parent = int(np.bincount(above).argmax()) + offsets[coarser]
                    break
            clusters.append(
                {"cluster": local + offsets[layer_index], "layer": layer_index, "parent": parent}
            )
    return point_cluster, clusters


def layers_from_tree(point_cluster: np.ndarray, clusters: list[dict]) -> list[np.ndarray]:
    """(points.cluster, clusters rows) -> per-layer label arrays (local labels, -1 noise)."""
    point_cluster = np.asarray(point_cluster)
    by_id = {row["cluster"]: row for row in clusters}
    n_layers = max(row["layer"] for row in clusters) + 1

    # Local label = rank of the global id within its layer.
    local = {}
    for layer_index in range(n_layers):
        ids = sorted(row["cluster"] for row in clusters if row["layer"] == layer_index)
        local.update({cluster_id: rank for rank, cluster_id in enumerate(ids)})

    layers = [np.full(point_cluster.shape[0], -1, dtype=np.int64) for _ in range(n_layers)]
    for point, cluster_id in enumerate(point_cluster.tolist()):
        while cluster_id is not None and cluster_id >= 0:
            row = by_id[cluster_id]
            layers[row["layer"]][point] = local[cluster_id]
            cluster_id = row["parent"]
    return layers
