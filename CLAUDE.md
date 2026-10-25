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
- `docs/papers/` — annotated bibliography of datamapping papers
  (`index.md`). The repo is used commercially: local PDFs in `pdfs/` only
  for CC BY/CC0 papers. Never copy in anything NC, ND, arXiv-default or
  publisher-copyright; link it with a short description instead.
- `tools/` — curation tools packaged as Agent Skills (symlinked into
  `.claude/skills/`). `tools/youtube-transcripts/` pulls talk transcripts +
  metadata into `docs/talks/`, driven by `docs/talks/by_tutte/talks.json`.
- `library/` — notes on specific techniques and papers.
- `images/` — assets used by the README.
- `repos/` — upstream git submodules, kept as reference code for how the
  tools are meant to be used. Don't edit these; they track upstream.
  - Pipeline stages: `vectorizers` (embed), `umap` + `pynndescent` (reduce),
    `hdbscan` / `fast_hdbscan` / `fast_plscan` / `evoc` (cluster), `toponymy` (name
    clusters), `datamapplot` + `glasbey` (render, colour palettes).
  - Examples and adjacent tools: `tutorials`, `thisnotthat` (interactive
    labeling), `temporal-mapper` (time-evolving maps).
  - Everything after `umap`/`hdbscan` is a shallow clone (`datamapplot` alone
    is ~900 MB).
  - A plain clone leaves `repos/*` empty. If they are, run
    `git submodule update --init` (it honours the shallow setting) before
    looking for reference code; don't conclude the code is missing.
  - Exception: in a git worktree (for example an implementer subagent's),
    never init the submodules; each init would copy about 2 GB. They are
    read-only reference, so read them from the main checkout instead: it is
    the parent folder of `git rev-parse --path-format=absolute --git-common-dir`,
    and the code is in its `repos/`.

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
