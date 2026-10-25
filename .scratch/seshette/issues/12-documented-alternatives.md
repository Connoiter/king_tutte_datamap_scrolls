# 12: Documented alternatives for each stage

**What to build:** Each scribe's instructions document its alternatives, so an agent can adapt when the default does not fit: the Embedder's all-MiniLM-L6-v2 lightweight fallback; the Reducer's openTSNE and PaCMAP; and the Clusterer's EVōC. The EVōC instructions state its three rules: build it with default parameters and never pass `approx_n_clusters`; read every layer from `cluster_layers_`, never `labels_` or the `fit_predict` result; and pass a fixed `random_state`. The Reducer still runs on the EVōC path, because EVōC gives no 2D coordinates.

**Blocked by:** 06 (Tracer bullet)

**Status:** ready-for-agent

- [ ] A run on the 500-row sample using EVōC as the Clusterer produces several cluster layers and passes the run checker.
- [ ] Each alternative is described with when to choose it, and its license is noted.
- [ ] No alternative changes `schema.sql`.

Spec: `.scratch/seshette/spec.md`. Glossary: `docs/terminology.md`.
