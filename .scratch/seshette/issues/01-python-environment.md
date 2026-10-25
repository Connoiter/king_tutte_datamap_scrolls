# 01: Python environment

**What to build:** A single `uv` project at the repo root, with pinned versions, that installs and imports everything the King Tutte pipeline needs on the target Mac (a modern Apple Silicon MacBook with 16 GB of memory or more): DuckDB, pyiceberg with its SQLite SQL catalog, pyarrow, sentence-transformers, UMAP, Toponymy (which brings `fast_hdbscan`), and DataMapPlot. Ollama is documented as the one extra install, with setup instructions for someone who has never installed a local model. Every later ticket runs inside this environment.

**Blocked by:** None (can start immediately)

**Status:** resolved

- [x] A fresh clone can create the environment with one `uv` command.
- [x] Every listed library imports without error inside it, on Apple Silicon.
- [x] Every library in the default path is permissively licensed, and the versions are pinned.
- [x] The Ollama install and model-pull steps are written down and have been followed once.

Spec: `.scratch/seshette/spec.md`. Glossary: `docs/terminology.md`.

## Answer

- **One command:** `uv sync` at the repo root (then `uv run pytest` to check). New files: `pyproject.toml` (non-package uv project), `uv.lock` (166 packages), `tests/test_environment.py`, `docs/setup.md`.
- **Python 3.12** (`requires-python = "==3.12.*"`), supported by every library; uv downloads it if missing.
- **Pinned direct deps:** datamapplot 0.7.3, duckdb 2.0.0, fast-hdbscan 0.3.2, pyarrow 26.0.0, pyiceberg[pyarrow,sql-sqlite] 0.12.0, sentence-transformers 5.7.0, toponymy 0.5.4, umap-learn 0.5.12; pytest 9.1.1 (dev group).
- **Test:** `tests/test_environment.py` imports every listed library, creates a namespace in a pyiceberg SQLite `SqlCatalog`, and imports `ToponymyClusterer` and `OllamaNamer`. 10 passed on an Apple M1 / 16 GB (about 90 s on first run, mostly numba compiling).
- **Licenses** (recorded in `docs/setup.md`): DuckDB MIT, pyiceberg Apache-2.0, pyarrow Apache-2.0, sentence-transformers Apache-2.0, UMAP BSD-3-Clause, Toponymy MIT, fast_hdbscan BSD-2-Clause, DataMapPlot MIT, Ollama MIT, Gemma 4 Apache-2.0.
- **Ollama:** steps written in `docs/setup.md` and followed on this machine: Ollama 0.40.11, `gemma4:e4b-it-qat` listed, a one-line `ollama run` prompt answered in about 6 s.
- **Surprises:**
  - Toponymy 0.5.4 caps `transformers<5` and sentence-transformers 6 needs `transformers>=5`, so an unpinned resolve quietly picks the older Toponymy 0.5.1. This repo pins Toponymy 0.5.4 (matching `repos/toponymy`), so sentence-transformers is 5.7.0 and transformers 4.57.6. Ticket 03 should confirm EmbeddingGemma 2 loads under transformers 4.57.
  - **Needs a human look:** DataMapPlot hard-depends on **pylabeladjust (GPL-3.0)**, and `import datamapplot` loads it (static-plot label placement, not the interactive HTML path). The direct libraries are all permissive, so the box is ticked, but strictly the default path pulls in one GPL package. Fine for local use; matters only if a bundle is redistributed. Also transitive: nose (LGPL, via Toponymy's apricot-select); certifi and tqdm (MPL-2.0).
