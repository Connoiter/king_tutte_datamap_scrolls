# 08: Search and click-through

**What to build:** A user can search the datamap by title, and click a point to open its source document. The Renderer always turns on DataMapPlot's search, and, when points have a `url`, passes the urls as extra point data so clicking a point opens it. Points without a url are not clickable. On the arXiv sample, each point's url is its arXiv abstract page.

**Blocked by:** 06 (Tracer bullet)

**Status:** ready-for-agent

- [ ] Searching a paper title in the HTML finds and highlights it.
- [ ] Clicking an arXiv point opens its abstract page.
- [ ] Only `title` and `url` from `documents` reach the HTML; document text does not.
- [ ] The run checker confirms search is on and the urls are present.

Spec: `.scratch/seshette/spec.md`. Glossary: `docs/terminology.md`.
