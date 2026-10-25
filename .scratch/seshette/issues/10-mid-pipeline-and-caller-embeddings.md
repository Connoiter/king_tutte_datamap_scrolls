# 10: Start mid-pipeline and caller-supplied embeddings

**What to build:** A caller can start the pipeline at any scribe whose inputs already exist. Each scribe first checks that its input tables exist and conform to `schema.sql`, and refuses with a clear message if they do not. In particular, a caller that already has embedding vectors writes `documents` and `embeddings` itself and skips the Embedder.

**Blocked by:** 06 (Tracer bullet)

**Status:** ready-for-agent

- [ ] A run that starts at the Reducer, with caller-written `documents` and `embeddings`, produces a datamap that passes the run checker in its mid-pipeline mode.
- [ ] Re-running from the Labeler or Renderer reuses earlier tables and leaves `documents` and `embeddings` untouched.
- [ ] Starting a scribe whose inputs are missing or malformed gives a clear refusal, not a crash.

Spec: `.scratch/seshette/spec.md`. Glossary: `docs/terminology.md`.
