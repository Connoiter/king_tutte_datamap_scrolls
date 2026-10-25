# 15: Fresh-session acceptance test

**What to build:** The supporting seam from the spec. In a new Claude Code session in this repo, with no history and no other instructions, a person runs `/datamap` on the 500-row sample. The run must pass the run checker within about 15 minutes on the target MacBook, and then a human opens the map and judges whether the cluster topics make sense. The human judgment is the part no script can do.

**Blocked by:** 07 (Real cluster labels), 08 (Search and click-through), 09 (Noise report)

**Status:** ready-for-human

- [ ] A fresh session completes `/datamap` on the 500-row sample with no help, in about 15 minutes or less.
- [ ] The run checker passes.
- [ ] A human records a judgment that the cluster topics make sense, with notes on any that do not.

Spec: `.scratch/seshette/spec.md`. Glossary: `docs/terminology.md`.
