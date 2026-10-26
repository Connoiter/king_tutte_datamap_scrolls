# 16: Extension pattern: open questions

**What to build:** Nothing yet. Decide the open design questions that the spec's "Architecture" and "Extending the pipeline" sections leave, then fold each answer back into the spec and, where a decision needs work, into new tickets. The spec documents the plan (scribes as sub-agents, playbooks as their briefings, side tables for extra data); this ticket holds what it does not settle.

**Blocked by:** none

**Status:** ready-for-human

Questions, each with the spec's current position:

1. **Who creates a side table?** The spec proposes: the table is declared in SQL shipped beside its scribe's playbook, created by the same DuckDB-then-pyiceberg route as the core tables, so a person chooses to add it and a running agent never invents one. The alternative, a scribe creating its table at run time, is simpler but lets agents drift the data format, which the core-schema rules exist to prevent. Confirm or change.
2. **Does the run checker validate side tables?** Options: core tables only; or also any side table declared by an installed playbook (checked for conformance, never required to exist). Decide, and say what the checker does when a declared side table is missing after a run that should have filled it.
3. **Does the core schema have versions?** The spec says `schema.sql` starts loose and is expected to change after the first real run. Decide whether pipelines and extensions record which core version they were built against, and how that relates to the Vectron Data Map Schema.
4. **What does the top-level file's line per scribe look like?** The spec says one line per scribe: what it produces, and which other scribes need to be told. Write the format, with a worked example for the cluster-description side table and the Renderer.
5. **Hosts without sub-agents.** The spec assumes Seshette can spawn a sub-agent per scribe. An Agent Skill may run on a host that cannot. A fallback is one agent reading the playbooks in turn, which loses the small-context benefit. Decide whether to support it, document it, or require sub-agents.
6. **Parallel scribes.** The spec allows scribes to run in parallel when they write only their own tables and do not read each other's output. Decide how Seshette knows this, for example from the top-level lines.
7. **Showing a cluster description in the web app.** DataMapPlot's tooltip is per point, and `extra_point_data` is one row per point, so a long cluster description stored there would repeat on every point in the cluster. Its `dynamic_tooltip` hooks (`fetch_js`, `format_js`, `loading_js`, `error_js`) might fetch a description lazily from a side file instead. Not read in detail, and not a design item now: a note for when someone builds it.
8. **Relative paths for side files.** Confirm the convention (paths relative to the `datamap/` folder, usable as URLs under a hosted copy) and whether the checker verifies that referenced files exist.

Checks before relying on the examples:

- Toponymy's namer can return a long description alongside the short label in one call. Look in `repos/toponymy`.
- The blog's pipeline diagram was described in conversation as drawing EVōC across both Reduce and Cluster. The spec says the Reducer still runs on the EVōC path, because EVōC gives no 2D coordinates (confirmed in its source and by its author). Confirm the two do not conflict, or note the difference in the glossary.

Parked: packaging cluster descriptions as concept documents in the Open Knowledge Format (OKF). Revisit separately; it is not part of the spec's extension pattern.

- [ ] Each question above has a recorded answer.
- [ ] The spec is updated to match, and the "proposed" wording on side-table creation is gone or confirmed.
- [ ] New tickets exist for any decision that needs work.

Spec: `.scratch/seshette/spec.md`. Glossary: `docs/terminology.md`.
