# 05: Datamap database and run checker

**What to build:** The real `schema.sql` for the four tables (documents, embeddings, points, clusters), shipped with the skill, and the step that creates an empty datamap database from it using the route experiment 02 settled. Every column later scribes fill is declared up front and nullable. Alongside it, a run checker: a test script outside the skill folder that checks a datamap database against the spec's primary-seam rules, and can be told which scribe a run started at, so only that scribe's outputs and later ones are checked.

**Blocked by:** 02 (Experiment: schema.sql to Iceberg tables)

**Status:** ready-for-agent

- [ ] `schema.sql` declares every table and column in the spec, and is the only place they are defined.
- [ ] An empty datamap database can be created from it in one step, with no hand-translation.
- [ ] The checker passes a correct hand-built database and fails databases that break each primary-seam rule (a missing points row, a cluster value that is neither real nor `-1`, an unlabeled non-noise cluster, a missing title).
- [ ] The checker never assumes a particular number of cluster layers.

Spec: `.scratch/seshette/spec.md`. Glossary: `docs/terminology.md`.
