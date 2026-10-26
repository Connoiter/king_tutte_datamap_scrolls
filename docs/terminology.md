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
toolkit and the orchestrator: a user or another skill (a caller) hands it data,
and she spawns scribes to run a King Tutte pipeline locally, handing each its
playbook and checking each handoff. It knows nothing about any particular
source format. _Avoid:_ "Seshat", "Sachet".

## Caller

Whoever invokes Seshette: a person typing `/datamap`, or a source-specific
skill in another repo that prepares the input and uses Seshette as a
component. The caller supplies each point's `id`, `text` and, optionally,
`title` and `url`.

## Scribe

A sub-agent that Seshette spawns to do one job, normally one pipeline stage. A
scribe is briefed by its playbook and nothing else, and reads from and writes
to the datamap database. A caller may start the pipeline at any scribe whose
inputs already exist. Added scribes (extensions) work the same way. _Avoid:_
"sub-skill"; a scribe is not a skill and not a file.

| Scribe | Stage | Default tool | Alternatives |
|---|---|---|---|
| Embedder | Embed | sentence-transformers with all-MiniLM-L6-v2 | EmbeddingGemma 2 |
| Reducer | Reduce | UMAP, to 2D map coordinates | openTSNE; PaCMAP |
| Clusterer | Cluster | Layered HDBSCAN on the 2D map (Toponymy's `ToponymyClusterer`) | EVōC |
| Labeler | Label | Toponymy with Gemma 4 via Ollama | |
| Renderer | Render | DataMapPlot | |

## Playbook

The markdown file inside the skill that is one scribe's whole briefing: its
job, the tables and columns it reads and writes, its default tool and
alternatives, and pointers to upstream example code. It is self-contained and
says nothing about how other scribes work, so the scribe's context window stays
small. Seshette reads playbooks only when she needs them. _Avoid:_
"instruction file", "sub-skill".

## Surveyor and Cartographer

The two-step overview of datamap production used on the Connoiter blog. The
Surveyor reduces dimensions and clusters (Reduce + Cluster); the Cartographer
labels and styles (Label + Render). Overview terms only: the scribes are named
after the five stages.

## Datamap database

The `datamap/` folder a run reads and writes: an Apache Iceberg database whose
catalog is a single SQLite file, with its tables stored as Parquet. It is the
only handoff between scribes. Its core table definitions live in `schema.sql`,
which scribes follow and never change.

## Side table

A table added by one extension scribe, keyed by the id it describes (for
example a cluster id), instead of new columns on a core table. It leaves the
core schema untouched and can be dropped without harm. Declared in SQL beside
the scribe's playbook. Large files, such as images, stay as files in the
`datamap/` folder, with a relative path in the side table.

## Documents table

`documents`: one row per point with `id`, `text`, an optional `title` and an
optional `url`, as supplied by the caller. Written once and never changed.
Only `title` and `url` reach the web page, where clicking a point opens its
`url`; `text` never does.

## Embeddings table

`embeddings`: one row per point with `id` and `high_d` (the original embedding
vector). Written once, by the caller or the Embedder. Large, so the vectors
are stored only here and never sent to the web page.

## Points table

`points`: one row per point with `id`, 2D coordinates `x, y`, `cluster` and
`title`. Small; scribes fill its columns in pipeline order. Every column is
declared in `schema.sql` from the start; scribes add data, never columns.

## Clusters table

`clusters`: one row per cluster, with a `cluster` id unique across all
cluster layers, its `layer`, its `parent` in the next coarser layer, and its
`label`. The rows form the cluster tree. A point's `cluster` is the finest
cluster it belongs to; its ancestors come from the tree.

## Title

A point's own short name, shown on hover. Usually supplied by the caller in
`documents.title`. The Labeler fills `points.title` for every point, copying
the caller's title or, for a point without one, the first 10 or so words of
its text. _Avoid:_
calling it a "label".

## Label

A cluster's name, written by the Labeler using Toponymy. Points get labels
only through their clusters.

## Cluster layer

One resolution of clustering. Layers are numbered from 0, the finest, upward
to the coarsest. The Clusterer produces several (how many depends on the
data), and the datamap shows them as zoom levels.

## Noise point

A point the Clusterer assigns to no cluster (`cluster = -1`). Noise points stay
on the map, drawn grey, and are never labeled.

## Vectron Data Map Schema

A planned standard Iceberg schema for datamaps, so any reader can load one.
`schema.sql` is its first draft. See
[Version one goals](https://connoiter.com/blog/version_one_goals/).
