# 13: README: using Seshette from another repo

**What to build:** The README gains a section on using Seshette from another repo: clone the Scrolls, symbolically link the skill folder into that repo's skills folder, and pull to update. It also says how that repo sets up its own Python environment. The upstream submodules the scribes' playbooks point to (EVōC, DataMapPlot, Toponymy, next to UMAP and HDBSCAN) are present and unedited.

**Blocked by:** 06 (Tracer bullet)

**Status:** ready-for-agent

- [ ] Following the README in a second, empty repo makes `/datamap` available there, and it runs.
- [ ] A pull of the Scrolls updates the linked skill with no other step.
- [ ] Every submodule the playbooks reference exists in the repo.

Spec: `.scratch/seshette/spec.md`. Glossary: `docs/terminology.md`.
