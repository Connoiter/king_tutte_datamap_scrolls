# 09: Noise report

**What to build:** At the end of every run, the top-level skill tells the user the share of points that are noise at each cluster layer (for example "layer 0: 34% grey, layer 3: 8% grey"), computed from `points` and the cluster tree with nothing new stored. If more than about half the points are noise at the finest layer, it explains that this is normal for HDBSCAN, names the setting to try (a lower `min_samples` on `ToponymyClusterer`), and offers to re-run from the Clusterer.

**Blocked by:** 06 (Tracer bullet)

**Status:** ready-for-agent

- [ ] Every run ends with a per-layer noise report.
- [ ] A run tuned to produce heavy noise triggers the explanation and the re-run offer.
- [ ] Accepting the offer re-runs only the Clusterer and later scribes, and the run checker passes.

Spec: `.scratch/seshette/spec.md`. Glossary: `docs/terminology.md`.
