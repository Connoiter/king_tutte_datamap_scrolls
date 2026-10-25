Status: ready-for-agent

# Seshette: the `/datamap` toolkit skill

## Problem Statement

People with a collection of documents, such as developers, researchers or
small-business owners, have no simple way to see what is in it. The King Tutte
pipeline (Embed → Reduce → Cluster → Label → Render) produces excellent
interactive datamaps, but assembling it means learning five separate libraries,
choosing models, tuning clustering, wiring data between stages, and often
paying for an LLM API to name the clusters. An AI coding agent could do this
work, but without a shared playbook every agent improvises a different, fragile
pipeline, and there is no agreed data format for handing work from one stage,
or one agent, to the next.

The Scrolls curate the right tools and know-how, but nothing yet turns them
into "datamap my data" for an agent or a person. Separately, source-specific
mappers built in other repos need a dependable component to build on instead of
re-implementing the pipeline.

## Solution

Seshette is a generic Agent Skill, triggered by `/datamap`, that lives in this
repo. A caller (a person or another skill) points it at a collection of
documents, or at documents that already have embeddings, and Seshette's five
scribes run a King Tutte pipeline locally, for free, on a modern Apple Silicon
MacBook. The result is an interactive standalone datamap web page plus a
datamap database that any later tool can read.

Version 1 is instructions only: the skill teaches the agent how to run each
stage, pointing it at the upstream example code curated in this repo, and the
agent writes and runs the code. Parts that prove stable will later move from
instructions into Python.

Scribes hand work to each other only through the datamap database, an Apache
Iceberg database whose tables are fixed by a SQL schema. The schema keeps every
agent on course: a scribe cannot write data the schema does not allow. Because
the database is the only handoff, a caller can start the pipeline at any
scribe, for example by supplying its own embeddings and skipping the Embedder.

The repo ships a worked example: a datamap of arXiv machine-learning paper
abstracts, produced by actually running Seshette, with the code the agent
generated committed alongside it.

## User Stories

1. As a developer with a folder of documents, I want to type `/datamap` and get an interactive map of my documents, so that I can see what topics my collection contains without learning five libraries.
2. As a small-business owner, I want to ask an agent to "datamap my data" in plain words, so that I can explore my documents without writing code.
3. As a user, I want the whole pipeline to run locally on my MacBook, so that my data never leaves my machine.
4. As a user, I want the pipeline to need no paid API keys or accounts, so that using it costs nothing.
5. As a user, I want a single setup step beyond the Python environment, installing Ollama, so that getting started is quick.
6. As a user, I want clear setup instructions for Ollama and the local models, so that I can get running even if I have never installed a local model before.
7. As a user, I want the output to be a standalone HTML file, so that I can open it in any browser or share it without a server.
8. As a user, I want to hover over a point and see its title, so that I know which document it represents.
9. As a user, I want clusters named with short, human-readable labels, so that I can read the map's topics at a glance.
10. As a user, I want coarse labels when zoomed out and finer labels when zoomed in, so that I can explore my collection at different levels of detail.
11. As a user, I want points that belong to no cluster to stay on the map, drawn grey, so that outliers are visible rather than silently dropped.
12. As a user whose documents have no titles, I want Seshette to give each point a short title anyway, so that hovering is always informative.
13. As a user with a very large collection of untitled documents, I want titling to fall back to each document's first line beyond a cap, so that a run does not take hours.
14. As a user, I want long documents embedded in full rather than cut off after a few hundred tokens, so that the map reflects whole documents.
15. As a caller that already has embedding vectors, I want to supply them and skip the Embedder, so that I don't pay to embed twice.
16. As a caller, I want to start the pipeline at any scribe whose inputs already exist, so that I can reuse earlier results or swap in my own stage.
17. As a caller, I want to supply each point's id, text and title, so that the map uses my own names for my documents.
18. As a source-specific skill in another repo, I want to use Seshette as a component rather than fork it, so that improvements to Seshette reach me automatically.
19. As a source-specific skill author, I want a written, schema-defined input format, so that I can build against Seshette before it has any Python code.
20. As a hackathon participant, I want to clone the Scrolls and link the skill into my own repo, so that I can use the latest Seshette with no packaging step.
21. As a hackathon participant, I want a pull of the Scrolls to update the skill I am using, so that fixes reach me immediately.
22. As an agent running a scribe, I want the database schema to reject data of the wrong shape, so that I cannot corrupt the work of earlier scribes.
23. As an agent running a scribe, I want each scribe's instructions to state exactly which tables and columns it reads and writes, so that I stay within my stage.
24. As an agent, I want each scribe to point me to curated upstream example code, so that I follow known-good usage instead of improvising.
25. As an agent, I want a sensible default tool for each stage, so that I don't stall on choices.
26. As an agent, I want documented alternatives for each stage, so that I can adapt when the default does not fit.
27. As an agent, I want the schema to be the single source of truth for the tables, so that I never maintain a second copy of the definitions.
28. As a maintainer, I want the schema to change only by a human decision, so that agents cannot drift the data format.
29. As a maintainer, I want large embedding vectors stored once in their own table, so that a run never copies gigabytes and the web page never downloads them.
30. As a maintainer, I want the database to be readable by tools other than the one that wrote it, so that a future Vectron client can load datamaps directly.
31. As a maintainer, I want every tool and model in the default path to be permissively licensed, so that the project stays a clean open-source example.
32. As a maintainer, I want the upstream libraries' example code available in this repo, so that agents learn from it rather than from memory.
33. As a maintainer, I want the worked example's generated code committed and labeled as generated, so that the example is genuinely runnable and seeds the later Python version.
34. As a maintainer, I want the worked example's whole datamap database committed while it is small, so that readers can inspect the tables without re-running anything.
35. As a learner, I want a README walkthrough of the worked example, including the exact `/datamap` request, so that I can reproduce it step by step.
36. As a learner, I want the pipeline stages named the same way in the skill, the glossary and the blog, so that I don't have to translate between vocabularies.
37. As a tester, I want a quick 500-document version of the example, so that I can iterate in minutes.
38. As a tester, I want a fixed random sample rather than the first rows, so that the test data is representative and identical on every run.
39. As a tester, I want a fresh agent session to succeed with `/datamap` alone, so that I know the skill works without this project's history.
40. As a future contributor, I want the scribes' contracts described in terms of database tables, so that I can reimplement any scribe in another language.
41. As a future contributor, I want stages whose default tool can be swapped (for example HDBSCAN for EVōC), so that the toolkit can grow without restructuring.
42. As a user exploring data with mixed media later, I want the default embedding model to support images and other media, so that adding them won't require changing models.

## Implementation Decisions

**Skill shape**
- Seshette is an Agent Skill named `datamap` (giving the `/datamap` trigger) in this repo. "Seshette" is its project name and appears in the skill's description.
- Version 1 contains instructions only, with no shipped Python. The agent reads the curated upstream example code in the repo, then writes and runs the pipeline code itself. Code moves into Python as the approach stabilizes.
- Seshette is generic: it has no knowledge of any source format. Source-specific mappers live in their own repos and call Seshette.
- The skill consists of a top-level instruction file plus one instruction file per scribe. A caller may start at any scribe; each scribe checks that its input tables exist and conform to the schema before running.

**Scribes (one per King Tutte pipeline stage)**

| Scribe | Stage | Default tool | Documented alternatives | Writes |
|---|---|---|---|---|
| Embedder | Embed | sentence-transformers with EmbeddingGemma 2 (text encoder, 768 dimensions) | all-MiniLM-L6-v2 as a lightweight fallback; TIMC Vectorizers for special cases | `inputs.high_d` |
| Reducer | Reduce | UMAP to 2D | | `points.x`, `points.y` |
| Clusterer | Cluster | EVōC | UMAP followed by HDBSCAN | `points.cluster`; the `clusters` table with every cluster layer and the cluster tree |
| Labeler | Label | Toponymy for cluster labels; the same local model for missing titles | | cluster labels; titles missing from `inputs` |
| Renderer | Render | DataMapPlot | | the standalone datamap HTML |

- EVōC produces cluster layers and a cluster tree but no 2D coordinates (confirmed in its source and by its author), so the Reducer always runs, even on the EVōC path.
- EVōC is the default Clusterer because it needs little tuning; UMAP + HDBSCAN is the documented alternative.
- The Embedder formats each document the way EmbeddingGemma 2 expects for documents, combining the title and text, and uses the plain document format when there is no title.
- The Labeler uses a local model, Gemma 4 (the `e4b` size; `e2b` if memory is tight), served by Ollama through Toponymy's Ollama namer. Paid APIs are documented only as optional upgrades, never as the default.
- Point titles are normally supplied by the caller. For points without one, the Labeler asks the same local model for a short title, of similar length to Toponymy's cluster labels, up to a cap of a few thousand points; above the cap, the title falls back to the first line of the text.
- Toponymy labels clusters only, never individual points. Noise points (cluster `-1`) are never labeled and are shown grey.
- Every cluster layer is labeled and kept, and the Renderer shows the layers as zoom levels.

**Datamap database**
- Each run reads and writes one datamap database: a folder named `datamap/` holding an Apache Iceberg database, with a pyiceberg SQL catalog stored as a single SQLite file inside the folder and table data stored as Parquet.
- Tables are defined once, as SQL `CREATE TABLE` statements in `schema.sql`, which ships with the skill. To create the Iceberg tables, DuckDB executes the SQL in memory only to derive the column types, and pyiceberg creates the real tables from those types. Neither the agent nor a script hand-translates the schema. Scribes never alter the schema; changing it is a human decision.
- Tables (first pass; precise column types are settled when `schema.sql` is written):
  - `inputs`: one row per point with `id`, `text`, `title`, `high_d`. Written once, by the caller or the Embedder. Never sent to the web page.
  - `points`: one row per point with `id`, `x`, `y`, `cluster`. Small; columns are filled in pipeline order.
  - `clusters`: one row per cluster per cluster layer, with its layer, parent cluster and label.
- All joins are by `id` (or by cluster and layer), never by row order.
- Scribes run strictly in sequence, so shared tables gain columns stage by stage with no concurrency concerns. Rewriting a small table is acceptable; the large `inputs` table is never rewritten.
- `schema.sql` is the first draft of the Vectron Data Map Schema.

**Scope limits for version 1** (matching Vectron v1): 2D maps only, one embedding per point, text only.

**Environment**
- Python runs locally through `uv`. Ollama is the one extra install. The hardware target is a modern Apple Silicon MacBook with 16 GB of memory or more.

**Repo additions**
- EVōC, DataMapPlot and Toponymy are added as upstream submodules next to UMAP and HDBSCAN, unedited, so agents learn from their example code. Licenses confirmed: EVōC BSD-2-Clause, DataMapPlot MIT, Toponymy MIT.
- The README gains a section on using Seshette from another repo: clone the Scrolls and symbolically link the skill folder into that repo's skills folder, then pull to update. No plugin packaging yet.

**Worked example**
- Dataset: arXiv ML paper abstracts (the `lmcinnes/arxiv_ml` dataset, CC0), with the paper title as each point's title. The dataset's own precomputed embeddings and coordinates are ignored; Seshette computes its own.
- Iterate on a fixed-seed random sample of 500 rows; the final committed run uses 5,000 rows.
- The example commits a README walkthrough (the exact `/datamap` request, what came out, how long each stage took), the code the agent generated during the run (one file per scribe, labeled as generated by Seshette), and the whole datamap database including the HTML.

## Testing Decisions

- Good tests check what a run leaves behind, not how a scribe got there. No test inspects a scribe's internals, such as UMAP parameters or the prompts sent to the model, so those stay free to change.
- **Primary seam: the datamap database after a run.** A run passes when:
  - every table conforms to `schema.sql`;
  - every `id` in `inputs` has exactly one row in `points`, with `x`, `y` and `cluster` all present;
  - every `cluster` value is either a real cluster or `-1`;
  - every non-noise cluster at every cluster layer has a label;
  - every point has a title;
  - the datamap HTML exists and opens in a browser.

  The same checks apply when a caller starts mid-pipeline; only the tables after the starting scribe are checked as outputs.
- **Supporting seam: the worked example in a fresh session.** A new Claude Code session in this repo runs `/datamap` on the 500-row sample with no other instructions. It passes when the primary-seam checks pass within about 15 minutes on the target MacBook, and a human opening the map judges that the cluster topics make sense. The human judgment is part of the test because label quality cannot be asserted automatically.
- Prior art: the repo has no tests yet. The upstream submodules have their own test suites, but those test the libraries, not Seshette.

## Out of Scope

- Source-specific mappers, including any mapper for a particular knowledge-bundle format. They live in their own repos and call Seshette.
- The separate Seshette web-service repo; this spec is unrelated to it.
- Shipping Python implementations of the scribes. Version 1 is instructions plus generated example code only.
- Packaging Seshette as a Claude Code plugin, or any formal distribution.
- 3D maps, multiple embeddings per point, and non-text media (images, audio, video).
- Paid LLM or embedding APIs as defaults.
- Comparing candidate models for labeling or embedding; that waits until the pipeline works end to end.
- Adding new points to an existing map without re-clustering (EVōC supports only fitting and predicting in one step).
- Reusing EVōC's nearest-neighbour graph to speed up UMAP.
- Finalizing the Vectron Data Map Schema.
- A hosted copy of the worked example's datamap.

## Further Notes

- **Untested assumptions, to check first when building:**
  - That DuckDB can derive column types from `schema.sql` cleanly enough for pyiceberg to create the tables, including the vector column.
  - That Gemma 4 `e4b` and the embedding model fit comfortably in memory together on a 16 GB MacBook.
  - That Toponymy's Ollama namer works with Gemma 4 and reliably gets the structured answers Toponymy expects.
- Toponymy's Ollama namer defaults to a Llama model, whose license is not permissive; Seshette must always name Gemma 4 explicitly.
- The schema intentionally starts loose ("first pass, don't sweat the details"); expect it to change after the first real run.
- Naming: the scribes are named after the five stages. "Surveyor" and "Cartographer" remain only as the blog's two-step overview. Spell the project name "Seshette".
- Background reading: the Connoiter blog posts on the data map pipeline, data map production and version one goals, and the Leland McInnes talk transcript curated under the docs talks folder.
