# 03: Experiment: both local models on 16 GB

**Type:** prototype

**What to build:** Answer the spec's second untested assumption: do Gemma 4 `e4b` (pulled through Ollama as the exact tag `gemma4:e4b-it-qat`, already installed on the target Mac) and EmbeddingGemma 2 (downloaded from Hugging Face, ungated) fit comfortably in memory together on a 16 GB MacBook? Load both at once, embed a few hundred arXiv abstracts with EmbeddingGemma 2 in the document format it expects, and ask Gemma 4 for a few short completions while the embedder is loaded. Record peak memory and throughput. If memory is tight, repeat with the fallback `gemma4:e2b-it-qat`.

**Blocked by:** 01 (Python environment)

**Status:** ready-for-agent

- [ ] Peak memory with both models loaded is recorded, along with embedding throughput (documents per second) and Gemma 4 response time.
- [ ] A recommendation is recorded: `gemma4:e4b-it-qat`, or `gemma4:e2b-it-qat` if needed.
- [ ] Neither model needed an account or API key to obtain.
- [ ] The findings are written under an `## Answer` heading in this file, and if they contradict the spec, the spec is updated (or a question raised for a human) before any ticket that depends on this one starts.

Spec: `.scratch/seshette/spec.md`. Glossary: `docs/terminology.md`.
