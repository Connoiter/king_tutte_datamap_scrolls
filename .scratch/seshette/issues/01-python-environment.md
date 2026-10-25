# 01: Python environment

**What to build:** A single `uv` project at the repo root, with pinned versions, that installs and imports everything the King Tutte pipeline needs on the target Mac (a modern Apple Silicon MacBook with 16 GB of memory or more): DuckDB, pyiceberg with its SQLite SQL catalog, pyarrow, sentence-transformers, UMAP, Toponymy (which brings `fast_hdbscan`), and DataMapPlot. Ollama is documented as the one extra install, with setup instructions for someone who has never installed a local model. Every later ticket runs inside this environment.

**Blocked by:** None (can start immediately)

**Status:** ready-for-agent

- [ ] A fresh clone can create the environment with one `uv` command.
- [ ] Every listed library imports without error inside it, on Apple Silicon.
- [ ] Every library in the default path is permissively licensed, and the versions are pinned.
- [ ] The Ollama install and model-pull steps are written down and have been followed once.

Spec: `.scratch/seshette/spec.md`. Glossary: `docs/terminology.md`.
