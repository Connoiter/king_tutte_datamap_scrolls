# 03: Experiment: both local models on 16 GB

**Type:** prototype

**What to build:** Answer the spec's second untested assumption: do Gemma 4 `e4b` (pulled through Ollama as the exact tag `gemma4:e4b-it-qat`, already installed on the target Mac) and EmbeddingGemma 2 (downloaded from Hugging Face, ungated) fit comfortably in memory together on a 16 GB MacBook? Load both at once, embed a few hundred arXiv abstracts with EmbeddingGemma 2 in the document format it expects, and ask Gemma 4 for a few short completions while the embedder is loaded. Record peak memory and throughput. If memory is tight, repeat with the fallback `gemma4:e2b-it-qat`.

**Blocked by:** 01 (Python environment)

**Status:** resolved

- [x] Peak memory with both models loaded is recorded, along with embedding throughput (documents per second) and Gemma 4 response time.
- [x] A recommendation is recorded: `gemma4:e4b-it-qat`, or `gemma4:e2b-it-qat` if needed.
- [x] Neither model needed an account or API key to obtain.
- [x] The findings are written under an `## Answer` heading in this file, and if they contradict the spec, the spec is updated (or a question raised for a human) before any ticket that depends on this one starts.

Spec: `.scratch/seshette/spec.md`. Glossary: `docs/terminology.md`.

## Answer

**Short version:** both models fit together on the 16 GB M1 and work at the
same time, but not "comfortably" on a Mac that is also running a normal
desktop: memory pressure goes to *warn* (with brief *critical* spikes while
Gemma loads) and swap grows by 1.5 to 3 GiB. Nothing failed or stalled. Keep
`gemma4:e4b-it-qat` as the default, load the embedder in bfloat16 with a small
batch, and document `gemma4:e2b-it-qat` as the fallback. **But EmbeddingGemma 2
does not load under the ticket 01 environment** (it needs transformers 5); see
Spec impact.

**Models.**
- Embedder: `google/embeddinggemma-2` (Hugging Face revision `914f7f89`),
  Apache-2.0, `gated: false`. Anonymous download confirmed: run with
  `HF_TOKEN` unset and `HF_HUB_DISABLE_IMPLICIT_TOKEN=1`, and an
  unauthenticated `curl` of `model.safetensors` redirects to the CDN as
  `user_id=public`. The checkpoint is one 1.49 GB multimodal file; loading text
  only (`config_kwargs={"vision_config": None, "audio_config": None}`) gives
  271 M parameters and 768-dimensional output.
- Labeler LLM: `gemma4:e4b-it-qat` (6.1 GB, already pulled) and
  `gemma4:e2b-it-qat` (4.3 GB, pulled for this test), both through Ollama
  0.40.11, no account; `ollama show --license` reports Apache 2.0.

**Method.** `experiments/03-models-in-memory/measure.py` (summary:
`summarize.py`): 400 arXiv ML abstracts (`lmcinnes/arxiv_ml`, first parquet
shard, `numpy` seed 42; data stays in the HF cache), formatted
`title: <title> | text: <abstract>` by the tested helper
`embedding_format.py`. Phases: embedder alone, Gemma alone, then both at once
(embedding in a thread while Gemma answers 8 distinct cluster-naming prompts,
until at least one full embedding pass is done). A sampler records every
0.5 s the macOS `phys_footprint` (Activity Monitor's "Memory", includes Metal
buffers) and RSS of this Python process and of the Ollama processes
(`ollama serve` + `llama-server` runner) separately, plus system available
memory, swap used and `kern.memorystatus_vm_pressure_level`. Per-process
numbers are unaffected by the concurrent ticket 02 job; the system numbers are
not. MPS, think disabled, `num_predict` 128.

**Baseline caveat.** Before anything was loaded this Mac already had 9.5 to
10 GiB of swap in use and only 3 to 6 GiB available (Chrome, the Claude app,
several Claude Code sessions, ticket 02). So the system-wide numbers are a
busy-desktop worst case, not a clean machine.

**Results, "both at once" phase** (footprint in GiB; per-process peaks):

| Run | Embedder | Ollama (RSS) | Sum | Embed docs/s alone / both | Gemma median response alone / both | Gemma tok/s alone / both | Min available | Swap growth | Pressure |
|---|---|---|---|---|---|---|---|---|---|
| e4b, embedder fp32, batch 16 | 4.1 to 4.5 | 6.7 (3.9) | 10.8 | 9.8 / 5.8 | 1.15 s / 1.03 s | 21 / 21 (drops to ~10 while sharing the GPU) | 0.8 | +3.2 (9.6 to 12.8) | warn; critical during Gemma load |
| e4b, embedder bf16, batch 4 | 2.2 | 6.7 (3.9) | 8.9 | 8.4 / 5.9 | 1.04 s / 1.59 s | 22 / 13 | 1.4 | +1.6 | warn; critical during Gemma load |
| e2b, embedder fp32, batch 16 | 4.1 to 4.6 | 1.3 (3.1) | 5.4 (about 7 counting RSS) | 9.9 / 7.3 | 0.59 s / 1.0 s | 42 / 21 | 2.0 | +0.3 | warn only |

- Peak memory with both loaded: about **9 to 11 GiB for e4b** (Ollama 6.7 +
  embedder 2.2 to 4.5), about **5.5 to 7 GiB for e2b**.
- Embedding throughput: **8 to 10 abstracts/s** alone, **6 to 7/s** while
  Gemma is generating (they share the GPU). 1,000 docs ~2 min; 100k docs
  ~3 hours on this machine.
- Gemma 4 e4b response time: **~7 to 8 s cold** (model load), then **~1 s**
  for a 130 to 170 token naming prompt with a 4 to 5 token answer; up to
  ~1.6 s while the embedder is busy. Answers were sensible short names
  ("Machine Learning Theory", "AI and Knowledge Systems").
- bfloat16 vs float32 embeddings on MPS: cosine >= 0.998, all finite. M1 has
  no native bf16, so fp32 is ~15% faster but twice the memory.

**Recommendation:** `gemma4:e4b-it-qat` stays the default. It fits and is fast
enough; the pressure seen is mostly the already-busy desktop. Load the
embedder in bfloat16 with `batch_size` 4 to 8 so its footprint stays near
2 GiB. Recommend `gemma4:e2b-it-qat` when the user's Mac has under ~10 GiB
available before the run (browser-heavy desktops), since it cuts the
Labeler's memory roughly in half and is twice as fast. Label quality of e2b vs
e4b was not evaluated (out of scope per the spec).

**Gotchas** (details for ticket 04 in the implementer notes):
- Needs transformers >= 5 (`embedding_gemma2` is unknown to 4.57.6:
  `ValueError: ... model type embedding_gemma2 but Transformers does not
  recognize this architecture`) and the checkpoint declares
  `sentence-transformers>=6.1.0`.
- Text-only loading still needs **torchvision** installed: the processor
  always builds `EmbeddingGemma2VideoProcessor`.
- The checkpoint leaves `max_seq_length` unbounded (~1e30); set it to 8192
  (the model's context) so long documents are not silently mishandled.
- Default dtype from the config is bfloat16 (on CPU too, where it warns it may
  be slow). Never use float16 (model card: NaNs). In transformers 5 the
  keyword is `dtype`, not `torch_dtype`.
- `format_document(text)` without a title gives exactly the model's own
  `prompt_name="Document"` prefix (`title: none | text: `; cosine 1.0); titled
  vs untitled embeddings of the same abstract differ (mean cosine 0.97), so the
  title matters.
- Ollama gave both Gemma 4 models a 4,096-token context by default here; a
  larger Toponymy prompt needs `num_ctx` raised, which costs memory.
- RSS badly undercounts under pressure (our process showed 0.1 GiB RSS with a
  4 GiB footprint, because macOS compressed it). Use `phys_footprint`.
  Conversely, Ollama's footprint excludes memory-mapped weights (e2b's
  `ollama ps` size is only 0.2 GiB, RSS 3.1 GiB).
- Python classes subclassing `threading.Thread` must not define `_stop`.

**Spec impact** (for the human; spec not edited):
1. EmbeddingGemma 2 cannot run in the ticket 01 environment. The spec's pins
   (Toponymy 0.5.4 + sentence-transformers, `docs/setup.md`) conflict:
   Toponymy 0.5.4 declares `transformers>=4.41,<5`, while EmbeddingGemma 2
   needs transformers 5 and sentence-transformers >= 6.1 (+ torchvision).
   Toponymy imports transformers only for its HuggingFace-pipeline namer, not
   for `OllamaNamer`; the upstream comment says the cap is "for compatibility
   with sentence-transformers". Options:
   - **A (recommended):** keep Toponymy 0.5.4 and add
     `[tool.uv] override-dependencies = ["transformers==5.20.2"]`, with
     `sentence-transformers==6.2.0` and `torchvision==0.29.1`. Verified here
     (in a scratch copy of the root project): it resolves, EmbeddingGemma 2
     runs, and `from toponymy import Toponymy, ToponymyClusterer` and
     `from toponymy.llm_wrappers import OllamaNamer` import under transformers
     5.20.2. A full Toponymy run under the override is untested (ticket 04).
   - B: Toponymy 0.5.1, which has no transformers cap (what an unpinned
     resolve picks), but is older and lacks 0.5.4's core litellm dependency.
   - C: fall back to all-MiniLM-L6-v2 as the default embedder (works with
     transformers 4.57), losing the 8K context and quality.
   A separate environment for the Embedder does not help, because the Labeler
   needs the same embedder in-process for Toponymy.
2. "Fit comfortably" holds only on a lightly loaded Mac: on a busy 16 GB
   desktop e4b + embedder pushes memory pressure to warn. Suggest the skill
   instructions check available memory before the Labeler and pick e2b below
   ~10 GiB, and load the embedder in bf16 with a small batch.

Reproduce: create a uv project identical to the root one but with
`sentence-transformers==6.2.0`, `torchvision`, `psutil` and
`override-dependencies = ["transformers==5.20.2"]`, then from the repo root
`uv run --project <that dir> python experiments/03-models-in-memory/measure.py
--dtype bfloat16 --batch-size 4 --out results.json` (add
`--model gemma4:e2b-it-qat` for the fallback) and
`python experiments/03-models-in-memory/summarize.py results.json`.
