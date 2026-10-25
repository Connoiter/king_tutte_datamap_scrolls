"""Estimate how many clusters ToponymyClusterer finds at 500 and 5,000 rows.

Labeling time scales with the number of clusters (one LLM call per cluster per
layer, plus disambiguation calls). To size the 500-row and 5,000-row runs
without embedding 5,000 abstracts, this uses the dataset's own precomputed
embeddings (a stand-in only; Seshette computes its own) with the same UMAP
and ToponymyClusterer settings as run_experiment.py.

    uv run --project <env> python experiments/04-toponymy-with-gemma/estimate_cluster_counts.py
"""

import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from cluster_tree import layers_from_tree, tree_from_layers  # noqa: E402
import pyarrow.parquet as pq
from huggingface_hub import hf_hub_download, list_repo_files

DATASET_ID = "lmcinnes/arxiv_ml"


def main():
    import umap
    from toponymy import ToponymyClusterer

    shard = sorted(
        f for f in list_repo_files(DATASET_ID, repo_type="dataset") if f.endswith(".parquet")
    )[0]
    table = pq.read_table(hf_hub_download(DATASET_ID, shard, repo_type="dataset"), columns=["embedding"])
    out = {}
    for n in (300, 500, 5000):
        idx = np.random.default_rng(42).choice(table.num_rows, size=n, replace=False)
        vectors = np.stack(table.take(sorted(idx)).column("embedding").to_numpy(zero_copy_only=False))
        vectors = vectors.astype(np.float32)
        coords = umap.UMAP(n_components=2, metric="cosine", random_state=42).fit_transform(vectors)
        # (base_min_cluster_size, min_clusters): run_experiment.py's settings,
        # then ToponymyClusterer's defaults.
        for base, min_clusters in ((5, 2), (10, 6)):
            try:
                clusterer = ToponymyClusterer(
                    base_min_cluster_size=base, min_clusters=min_clusters
                ).fit(coords, vectors)
                counts = [int(x.cluster_labels.max()) + 1 for x in clusterer.cluster_layers_]
                labels = [x.cluster_labels for x in clusterer.cluster_layers_]
                point_cluster, clusters = tree_from_layers(labels)
                rebuilt = layers_from_tree(point_cluster, clusters)
                layer_of = {row["cluster"]: row["layer"] for row in clusters}
                result = {
                    "clusters_per_layer": counts,
                    "total": sum(counts),
                    # Does the parent-pointer tree lose anything? (strict nesting)
                    "round_trip_points_changed": [int(np.sum(a != b)) for a, b in zip(labels, rebuilt)],
                    "parents_skipping_a_layer": sum(
                        1
                        for row in clusters
                        if row["parent"] is not None
                        and layer_of[row["parent"]] != row["layer"] + 1
                    ),
                }
            except ValueError as e:
                result = {"error": str(e)}
            out[f"n={n} base={base} min_clusters={min_clusters}"] = result
            print(n, base, min_clusters, result, flush=True)
    print(json.dumps(out))


if __name__ == "__main__":
    main()
