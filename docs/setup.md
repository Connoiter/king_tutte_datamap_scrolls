# Setup

How to get a machine ready to run a King Tutte pipeline from this repo.
The target is a modern Apple Silicon MacBook with 16 GB of memory or more.

There are two installs: the Python environment (one `uv` command) and
Ollama (the one extra install, which serves the local model that names
clusters).

## 1. Python environment

Install [uv](https://docs.astral.sh/uv/) if you don't have it
(`brew install uv`), then from the repo root:

```sh
uv sync
```

That creates `.venv/` with Python 3.12 (uv downloads it if needed) and the
exact versions recorded in `uv.lock`. It is about 1.5 GB, mostly PyTorch.

Check it worked:

```sh
uv run pytest
```

The first run takes a minute or two: numba compiles UMAP's and
`fast_hdbscan`'s kernels on first import and caches them. Later runs are
faster.

Run any pipeline code the same way, with `uv run python ...`.

### What is in it

| Library | Pinned | Role | License |
| --- | --- | --- | --- |
| [DuckDB](https://github.com/duckdb/duckdb) | 2.0.0 | Derive column types from `schema.sql` | MIT |
| [pyiceberg](https://github.com/apache/iceberg-python) (`sql-sqlite`, `pyarrow` extras) | 0.12.0 | Datamap database (Iceberg tables, SQLite catalog) | Apache-2.0 |
| [pyarrow](https://github.com/apache/arrow) | 26.0.0 | Table data (Parquet) | Apache-2.0 |
| [sentence-transformers](https://github.com/huggingface/sentence-transformers) | 5.7.0 | Embedder | Apache-2.0 |
| [UMAP](https://github.com/lmcinnes/umap) (`umap-learn`) | 0.5.12 | Reducer | BSD-3-Clause |
| [Toponymy](https://github.com/TutteInstitute/toponymy) | 0.5.4 | Clusterer (`ToponymyClusterer`) and Labeler (`OllamaNamer`) | MIT |
| [fast_hdbscan](https://github.com/TutteInstitute/fast_hdbscan) | 0.3.2 | Layered HDBSCAN under `ToponymyClusterer` | BSD-2-Clause |
| [DataMapPlot](https://github.com/TutteInstitute/datamapplot) | 0.7.3 | Renderer | MIT |

Notable transitive dependencies: PyTorch (BSD-3-Clause), transformers
4.57.6 (Apache-2.0), litellm (MIT; Toponymy's `OllamaNamer` is a litellm
wrapper), numba / llvmlite (BSD-2-Clause), pynndescent (BSD-2-Clause).
`uv.lock` pins all 166 packages.

Why sentence-transformers 5.x and not 6.x: Toponymy 0.5.4 requires
`transformers<5`, and sentence-transformers 6 requires `transformers>=5`.
Letting uv choose freely gives sentence-transformers 6 with the older
Toponymy 0.5.1 instead; this repo prefers the current Toponymy, which matches
the reference code in `repos/toponymy`.

### License caveats

Every library above is permissively licensed. A few transitive dependencies
are not, and are worth knowing about:

- **pylabeladjust (GPL-3.0)** is a required dependency of DataMapPlot, and
  `import datamapplot` imports it (through `plot_rendering` and
  `text_placement`). DataMapPlot uses it to place labels on its static
  matplotlib plots, not in the interactive HTML that Seshette renders, but it
  is installed and loaded either way. Running it locally is fine; it matters
  only if you redistribute a bundle that includes it.
- **nose (LGPL)** comes in through Toponymy's `apricot-select` dependency.
- **certifi** and **tqdm** are MPL-2.0 (file-level weak copyleft), which is
  usually treated as fine for this kind of use.

## 2. Ollama and the local model

[Ollama](https://ollama.com) (MIT) runs language models on your own machine.
Seshette uses it to serve Gemma 4, which writes the cluster labels. No
account or API key is needed, and nothing is sent to the internet once the
model is downloaded.

### Install Ollama

Either download the macOS app from <https://ollama.com/download> and drag it
into Applications, or use Homebrew:

```sh
brew install ollama
```

Start it. The app starts a background server when you open it (you'll see a
llama icon in the menu bar). With Homebrew, run `brew services start ollama`,
or `ollama serve` in a terminal you leave open.

Check that it is running:

```sh
ollama --version
```

### Download the model

```sh
ollama pull gemma4:e4b-it-qat
```

This downloads about 6.1 GB once. Use this exact tag: `-it-qat` is the
quantization-aware-trained instruction model. The plain `gemma4:e4b` tag may
pull a larger build.

If memory is tight (Ollama errors, or the machine swaps heavily while the
pipeline runs), use the smaller fallback instead:

```sh
ollama pull gemma4:e2b-it-qat   # about 4.3 GB
```

Gemma 4 is Apache-2.0. Name it explicitly wherever a model is chosen:
Toponymy's `OllamaNamer` defaults to a Llama model, whose license is not
permissive.

### Check the model works

```sh
ollama list
ollama run gemma4:e4b-it-qat "Reply with exactly three words naming this topic: umap, hdbscan, clustering."
```

`ollama list` should show `gemma4:e4b-it-qat`, and the second command should
print a short answer within a few seconds (the first call loads the model
into memory, so it is the slowest).

These steps were last followed on an Apple M1 with 16 GB, Ollama 0.40.11:
the prompt above answered "Dimensionality Reduction Clustering" in about six
seconds.

## Models downloaded on first use

The embedding model (EmbeddingGemma 2, Apache-2.0) is not part of either
install. sentence-transformers downloads it from Hugging Face the first time
the Embedder runs; it is not gated, so no account is needed.
