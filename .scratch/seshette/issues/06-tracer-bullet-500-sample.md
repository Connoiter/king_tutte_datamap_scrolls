# 06: Tracer bullet: /datamap on the 500-row arXiv sample

**What to build:** The first end-to-end King Tutte pipeline. The `datamap` skill exists, with a top-level instruction file and one instruction file per scribe, each stating exactly which tables and columns it reads and writes, and pointing to curated upstream example code. A person runs `/datamap` on a fixed-seed random sample of 500 rows of the `lmcinnes/arxiv_ml` dataset. Acting as a caller, the agent writes the sample into `documents` (paper title as title), then the scribes run the default tools: the Embedder with EmbeddingGemma 2; the Reducer with UMAP to 2D with a fixed `random_state`; the Clusterer with `ToponymyClusterer` on the 2D map, storing the cluster tree as parent pointers with layer 0 the finest; a minimal Labeler that fills `points.title` and writes placeholder labels such as "Cluster 12"; and the Renderer, which builds DataMapPlot's per-layer label arrays in memory, maps noise to DataMapPlot's `noise_label` so it draws grey, and writes a standalone datamap HTML with the layers as zoom levels.

**Blocked by:** 03 (Experiment: both local models on 16 GB), 05 (Datamap database and run checker)

**Status:** ready-for-agent

- [ ] Running `/datamap` on the 500-row sample produces a datamap database and a standalone HTML file.
- [ ] The run checker passes on the result.
- [ ] The HTML opens in a browser: hovering shows titles, zooming changes cluster layers, and noise points are grey.
- [ ] Running it again with the same seed gives the same map.
- [ ] The skill's description names Seshette, and it triggers on `/datamap`.

Spec: `.scratch/seshette/spec.md`. Glossary: `docs/terminology.md`.
