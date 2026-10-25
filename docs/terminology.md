# Terminology

Project-specific nouns used throughout the King Tutte Datamap Scrolls. When
writing docs, specs or code, use these terms as defined here and avoid the
listed synonyms.

## Datamap

An interactive visualization of a collection of embedding vectors: points on a
2D map, grouped into labeled clusters, explorable in a web browser. Spelled as
one word, like "dataset" and "datapoint". _Avoid:_ "data map".

## King Tutte pipeline

A chain of permissively licensed tools, mostly from the Tutte Institute (UMAP,
HDBSCAN, EVōC, Toponymy, DataMapPlot, ...), that turns a collection of
documents or embedding vectors into a datamap. It has five stages: Embed,
Reduce, Cluster, Label, Render. See the
[King Tutte data map pipeline](https://connoiter.com/blog/king_tutte_data_map_pipeline/)
post.

## Seshette

The generic datamapping Agent Skill in this repo, triggered by `/datamap`.
Named as a variant of [Seshat](https://en.wikipedia.org/wiki/Seshat), the
Egyptian goddess of writing and "mistress of the house of books". Seshette is a
toolkit: a user or another skill (a caller) hands it data, and its scribes run
a King Tutte pipeline locally. It knows nothing about any particular source
format. _Avoid:_ "Seshat", "Sachet".

## Caller

Whoever invokes Seshette: a person typing `/datamap`, or a source-specific
skill in another repo that prepares the input and uses Seshette as a
component. The caller supplies each point's `id`, `text` and, optionally,
`title`.

## Scribe

One of Seshette's sub-skills, one per pipeline stage. Each scribe reads from
and writes to the datamap database. A caller may start the pipeline at any
scribe whose inputs already exist.

| Scribe | Stage | Default tool | Alternatives |
|---|---|---|---|
| Embedder | Embed | sentence-transformers with EmbeddingGemma 2 | all-MiniLM-L6-v2; TIMC Vectorizers for special cases |
| Reducer | Reduce | UMAP, to 2D map coordinates | |
| Clusterer | Cluster | EVōC | UMAP + HDBSCAN |
| Labeler | Label | Toponymy with Gemma 4 via Ollama | |
| Renderer | Render | DataMapPlot | |

## Surveyor and Cartographer

The two-step overview of datamap production used on the Connoiter blog. The
Surveyor reduces dimensions and clusters (Reduce + Cluster); the Cartographer
labels and styles (Label + Render). Overview terms only: the scribes are named
after the five stages.

## Datamap database

The `datamap/` folder a run reads and writes: an Apache Iceberg database whose
catalog is a single SQLite file, with its tables stored as Parquet. It is the
only handoff between scribes. Its table definitions live in `schema.sql`, which
scribes follow and never change.

## Inputs table

`inputs`: one row per point with `id`, `text`, `title` and `high_d` (the
original embedding vector). Written once, by the caller or the Embedder. Large,
so it is never sent to the web page.

## Points table

`points`: one row per point with `id`, 2D coordinates `x, y`, and `cluster`.
Small; scribes add columns to it in pipeline order.

## Clusters table

`clusters`: one row per cluster per cluster layer, with its parent in the
cluster tree and its label.

## Title

A point's own short name, shown on hover. Usually supplied by the caller; the
Labeler writes one only for points that arrive without a title. _Avoid:_
calling it a "label".

## Label

A cluster's name, written by the Labeler using Toponymy. Points get labels
only through their clusters.

## Cluster layer

One resolution of clustering, from fine to coarse. EVōC produces several, and
the datamap shows them as zoom levels.

## Noise point

A point the Clusterer assigns to no cluster (`cluster = -1`). Noise points stay
on the map, drawn grey, and are never labeled.

## Vectron Data Map Schema

A planned standard Iceberg schema for datamaps, so any reader can load one.
`schema.sql` is its first draft. See
[Version one goals](https://connoiter.com/blog/version_one_goals/).
