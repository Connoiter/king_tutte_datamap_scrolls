# 07: Real cluster labels with Gemma 4

**What to build:** Replace the tracer bullet's placeholder labels with real ones. The Labeler hands Toponymy the Clusterer's layers and tree from the datamap database, uses Gemma 4 through Ollama via `OllamaNamer`, always naming the exact tag `gemma4:e4b-it-qat` (or `gemma4:e2b-it-qat` if experiment 03 recommended the fallback), and writes a label for every non-noise cluster at every cluster layer. Paid APIs are documented only as optional upgrades.

**Blocked by:** 04 (Experiment: Toponymy with Gemma 4), 06 (Tracer bullet)

**Status:** ready-for-agent

- [ ] On the 500-row sample, every non-noise cluster at every layer has a Toponymy label, and the run checker passes.
- [ ] Coarse layers show broader labels than fine layers when zooming.
- [ ] No paid API key or account is used anywhere in the run.

Spec: `.scratch/seshette/spec.md`. Glossary: `docs/terminology.md`.
