# 04: Experiment: Toponymy with Gemma 4

**Type:** prototype

**What to build:** Answer the spec's third untested assumption: does Toponymy's `OllamaNamer`, explicitly set to Gemma 4 (never its Llama default), reliably get the structured answers Toponymy expects? Also confirm the hand-off the Labeler will use: Toponymy is given cluster layers and a cluster tree that already exist, and does not cluster again. Use a small sample clustered with `ToponymyClusterer`, and the Embedder's model as Toponymy's text embedding model.

**Blocked by:** 03 (Experiment: both local models on 16 GB)

**Status:** ready-for-agent

- [ ] Toponymy has produced a label for every non-noise cluster at every cluster layer of the sample, using Gemma 4, or the failures are recorded with examples.
- [ ] Toponymy accepted precomputed cluster layers and a cluster tree without re-clustering.
- [ ] Labeling time per cluster is recorded, to size the time budget for the 500-row and 5,000-row runs.
- [ ] The findings are written under an `## Answer` heading in this file, and if they contradict the spec, the spec is updated (or a question raised for a human) before any ticket that depends on this one starts.

Spec: `.scratch/seshette/spec.md`. Glossary: `docs/terminology.md`.
