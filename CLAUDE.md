# King Tutte Datamap Scrolls

A curation/documentation repo (not an application) for building "King Tutte
pipelines": permissively licensed open source toolchains, mostly from the Tutte
Institute (UMAP, HDBSCAN, DataMapPlot, Toponymy, EVōC, ...), that turn
collections of embedding vectors into interactive datamaps.

The goal is Seshette, a generic `/datamap` Agent Skill: point it at a
collection of documents (or embeddings) and it runs a King Tutte pipeline
locally to produce an interactive datamap. Source-specific mappers live in
their own repos and use Seshette as a component; keep source-specific
material out of this repo.

## References


The Connoiter blog is the main documentation for what a King Tutte Pipeline is:
https://connoiter.com/blog/


## Layout

- `Readme.md` — the main narrative and project direction.
- `docs/terminology.md` — descriptions of various project specific nouns.
- `docs/agents/` — configuration for Matt Pocock's engineering skills.
- `.scratch/` — specs and issues (the local-markdown issue tracker).
- `docs/talks/` — curated datamapping tech talks.
  - TODO: A very early work in progress
- `library/` — notes on specific techniques and papers.
- `images/` — assets used by the README.
- `repos/` — upstream git submodules (`umap`, `hdbscan`). Don't edit these;
  they track upstream.

## Conventions

- Only curate material that is permissively licensed, and credit/cite upstream sources.
- There's no integrated pipeline yet, so don't describe one as runnable unless
  the code for it is actually in the repo.

## Agent skills

### Issue tracker

Issues and specs live as local markdown files under `.scratch/<feature>/`. See `docs/agents/issue-tracker.md`.

### Triage labels

The five default triage roles, recorded as a `Status:` line in each issue file. See `docs/agents/triage-labels.md`.

### Domain docs

Single-context; the glossary is `docs/terminology.md`. See `docs/agents/domain.md`.
