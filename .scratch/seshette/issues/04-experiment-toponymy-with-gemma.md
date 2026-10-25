# 04: Experiment: Toponymy with Gemma 4

**Type:** prototype

**What to build:** Answer the spec's third untested assumption: does Toponymy's `OllamaNamer`, explicitly set to Gemma 4 as `gemma4:e4b-it-qat` (never its Llama default; use `gemma4:e2b-it-qat` instead if experiment 03 recommends it), reliably get the structured answers Toponymy expects? Also confirm the hand-off the Labeler will use: Toponymy is given cluster layers and a cluster tree that already exist, and does not cluster again. Use a small sample clustered with `ToponymyClusterer`, and the Embedder's model as Toponymy's text embedding model.

**Blocked by:** 03 (Experiment: both local models on 16 GB)

**Status:** resolved

- [x] Toponymy has produced a label for every non-noise cluster at every cluster layer of the sample, using Gemma 4, or the failures are recorded with examples.
- [x] Toponymy accepted precomputed cluster layers and a cluster tree without re-clustering.
- [x] Labeling time per cluster is recorded, to size the time budget for the 500-row and 5,000-row runs.
- [x] The findings are written under an `## Answer` heading in this file, and if they contradict the spec, the spec is updated (or a question raised for a human) before any ticket that depends on this one starts.

Spec: `.scratch/seshette/spec.md`. Glossary: `docs/terminology.md`.

## Answer

**Short version:** yes, with two settings OllamaNamer does not set by itself.
Out of the box, Toponymy + `OllamaNamer(model="gemma4:e4b-it-qat")` failed on
**every** call (42 of 42) and `Toponymy.fit` still returned normally, with every
label an empty string. With `provider_kwargs={"think": False, "num_ctx": 16384}`
it labeled every cluster at every layer with **0 parse failures in 19 calls**.
The precomputed-cluster hand-off works and Toponymy did not re-cluster. The full
path also runs under transformers 5 (ticket 03's override env).

**Method.** `experiments/04-toponymy-with-gemma/run_experiment.py`: 300
abstracts from `lmcinnes/arxiv_ml` (first parquet shard, `default_rng(42)`, same
sampling as 03), embedded with EmbeddingGemma 2 (bf16, MPS, batch 4,
`title: … | text: …`), UMAP 2D (`metric="cosine"`, `random_state=42`),
`ToponymyClusterer(base_min_cluster_size=5, min_clusters=2)` → 2 layers (13 and
3 clusters; 37% / 7% noise). The layers go to the schema's shape
(`points.cluster` + `clusters` rows with parent pointers) and back with the
tested helper `cluster_tree.py`, and are wrapped in `PrecomputedClusterer`
(`precomputed_clusterer.py`, tested). Then `Toponymy(llm_wrapper=OllamaNamer(…),
text_embedding_model=<the same EmbeddingGemma 2 object>, clusterer=<precomputed>)
.fit(texts, vectors, coords)`. A small logging proxy between litellm and Ollama
records every request body and raw response; the namer's debug `callback`
records parse results. Tests: `uv run --project <env> pytest
experiments/04-toponymy-with-gemma` (7 pass). Raw results (not committed):
`run04_gemma/` (final), `run04_gemma_think_default/`, `run04_gemma_ctx4096/` in
the session scratchpad.

**Labels** (final run, think off, 16K context):
- Layer 0 (13/13 labeled), e.g. "Formal Semantics for Multi-Agent Epistemic and
  Temporal Knowledge Representation", "Probabilistic Modeling and Efficient
  Architectures for Robust Speech Recognition Systems", "Computational
  Complexity of Algebraic Varieties and Polynomial System Solving", "Heuristic
  Algorithms for NP-Hard Constraint Satisfaction and Optimization Problems".
- Layer 1 (3/3 labeled): "Optimization Algorithms", "Deep Learning Vision", and
  "Semantic Information Retrieval and Content Analysis from Web and Social
  Media Data" (a layer-1 cluster with a single child; Toponymy copies the
  child's name without an LLM call). Coarse layers get 1-2 word names by
  Toponymy's design (detail level per layer).
- Sensible topics for the sample.

**What OllamaNamer sends** (toponymy 0.5.4 → litellm 1.103.9 `ollama_chat` →
`POST /api/chat`, plus one `/api/show`):
`{"model": "gemma4:e4b-it-qat", "options": {"temperature": 0.4, "num_predict": 128}, "stream": false, "format": "json"}`
with a system and a user message. So: structured output is Ollama's
`format: "json"` (JSON mode, no schema); answers are parsed by regex
(`GET_TOPIC_NAME_REGEX`, `GET_TOPIC_CLUSTER_NAMES_REGEX`) then `json.loads`.
No `think` and no `num_ctx` are sent.

**Failures and fixes:**
1. **Thinking (100% failure).** Gemma 4 thinks by default; with no `think`
   field every response spent all 128 `num_predict` tokens on
   `message.thinking` and returned `content: ""` (`done_reason: "length"`).
   Example thinking, cut at 128 tokens: "*   Keywords: logic, formalization
   using, multi-agent only-knowing, revision operators…". The regex finds
   nothing (`IndexError: list index out of range`), tenacity retries 3 times
   with 4-10 s waits, Toponymy re-runs the empty ones once more (42 calls for
   7 clusters), then **keeps `""` as the name with only a `UserWarning`**:
   `fit` succeeds, 7 of 7 labels empty, 574 s wasted. Fix:
   `OllamaNamer(..., provider_kwargs={"think": False})`; litellm forwards it as
   top-level `"think": false` (`reasoning_effort="none"` does the same).
2. **Context truncation (9 of 11 disambiguation calls failed).** With think
   off, all 15 topic-name calls parsed, but Ollama's default context here is
   4,096 tokens and Toponymy's disambiguation prompts (`generate_topic_cluster_names`,
   20-34K characters, 3.9-6.3K tokens) were silently truncated
   (`prompt_eval_count` stuck at 2,051 for prompts of 21K and 41K characters).
   Gemma lost the output instructions and answered a flat dict instead of
   `{"new_topic_name_mapping": …, "topic_specificities": …}`, e.g.
   `{"Video Transfer Learning": "Leveraging Image Knowledge for Robust Video Recognition with Limited Data", "Adversarial Robustness": "Internal Projection for Adversarial Resilience in Neural Networks", …}`
   or `{"topic_1": "…", "topic_2": "…"}`. After retries Toponymy keeps the old
   (duplicate) names, again with only a warning. Fix: add `"num_ctx": 16384`
   to `provider_kwargs`; litellm puts it in Ollama's `options` and Ollama
   reloads the model with a 16,384-token context. Result: 4 of 4
   disambiguation calls parsed, 0 failures overall.
- Topic-name prompts are ~1.2-2.3K tokens (8 full abstracts as exemplars);
  answers 20-33 tokens. No thinking in any final-run response.

**No re-clustering, confirmed two ways:**
- Source (toponymy 0.5.4 `toponymy.py`, `Toponymy.fit`): if
  `hasattr(self.clusterer, "cluster_layers_") and hasattr(self.clusterer, "cluster_tree_")`
  it copies both and never calls `fit_predict`.
- Runtime: `PrecomputedClusterer.fit` / `fit_predict` raise; spies on
  `toponymy.clustering.build_raw_cluster_layers`, `create_cluster_layers` and
  `ToponymyClusterer.fit` counted 0 calls during `Toponymy.fit`; and
  `topic_model.cluster_layers_ is pre.cluster_layers_`.
- Gotcha for the Labeler: on this path Toponymy does not pass its
  `prompt_template` to the layers, so the wrapper must build the layers with
  `prompt_template=PROMPT_TEMPLATES` and the exemplar delimiters itself (as
  `PrecomputedClusterer` does).
- Round trip layers → schema tree → layers was exact (0 points changed per
  layer), and Toponymy's `build_cluster_tree` on the rebuilt layers equals the
  clusterer's `cluster_tree_`. Also exact on 300/500/5,000-point stand-in maps
  with 1-5 layers (`estimate_cluster_counts.py`), so the layers do nest
  strictly. **But parents often skip a layer** (see Spec impact).

**Timing** (16 GB M1, busy desktop, e4b, embedder bf16 batch 4 loaded):
- `Toponymy.fit`: **387 s for 16 clusters = 24 s per cluster** (LLM 321 s,
  embedder 61 s encoding 5,602 keyphrases, rest ~5 s). Topic-name calls 8-14 s
  each (prompt evaluation of ~2K tokens dominates; ~30 output tokens);
  disambiguation calls 26-44 s. Before the pipeline: embed 37 s, UMAP 5 s,
  cluster 1 s.
- Cluster counts for extrapolation (`estimate_cluster_counts.py`, the dataset's
  own embeddings as a stand-in, which gave 26 clusters at 300 rows where
  EmbeddingGemma 2 gave 16): 500 rows → 23-39 clusters; 5,000 rows → 177-335
  clusters (ToponymyClusterer defaults vs base 5 / min_clusters 2).
- **Extrapolated Labeler time at ~24 s/cluster: 500 rows ≈ 6-16 min; 5,000
  rows ≈ 1-2.2 hours.** Untested speedups: fewer/shorter exemplars (prompt
  size drives time), `gemma4:e2b-it-qat` (~2x faster in 03), a larger embedder
  batch for keyphrases.

**Transformers 5 verdict:** the full labeling path (ToponymyClusterer +
Toponymy.fit with OllamaNamer + EmbeddingGemma 2 as text embedding model) works
under transformers 5.20.2 / sentence-transformers 6.2.0 / toponymy 0.5.4 via
`override-dependencies` (ticket 03's scratch env, root pins untouched). No
errors or warnings from transformers. The MiniLM fallback was therefore not
needed. This supports ticket 03's option A; the pin decision is still the
human's.

**Spec impact** (for the human; spec not edited):
1. The Labeler instructions must set `OllamaNamer(model="gemma4:e4b-it-qat",
   provider_kwargs={"think": False, "num_ctx": 16384})`. Without `think`, every
   label is empty; without `num_ctx`, disambiguation silently fails. Memory
   cost of the 16K context was not measured (03 measured 4K).
2. Toponymy records a failed label as `""` and `fit` succeeds. The checker's
   "every non-noise cluster has a label" must treat an empty string as missing,
   and the Labeler should check for empty names after `fit`.
3. The spec says `clusters.parent` is "its parent cluster in the next coarser
   layer". In practice a parent is in the **nearest coarser layer where the
   cluster is not noise**, which can skip layers (4 of 26 clusters at 300 rows,
   50 of 335 at 5,000 on the stand-in; Toponymy's own `build_cluster_tree` does
   the same). Nesting is strict, so parent pointers lose nothing; only the
   wording (and any checker assumption) needs to change.
4. At 300 rows `ToponymyClusterer` defaults (`base_min_cluster_size=10`,
   `min_clusters=6`) give a single layer, so no zoom levels; 500 rows gave 2
   layers on the stand-in. The 500-row tracer may want `min_clusters` lowered.
5. `ToponymyClusterer` calls `parallel_boruvka(..., reproducible=False)`; two
   identical runs on the same 5,000-point map gave 225 vs 226 layer-0
   clusters. A fixed UMAP `random_state` does not make clustering fully
   repeatable, which matters for "comes out the same on every run".
6. Labeling time: 500 rows ≈ 6-16 min of labeling alone, which makes the
   15-minute fresh-session target tight; 5,000 rows ≈ 1-2 hours.
7. Open: Toponymy embeds keyphrases and topic names with the raw embedder (no
   EmbeddingGemma prompt prefix) and compares them with document vectors made
   with the document prefix. It worked here; whether a query prefix improves
   keyphrases was not tested.

## Comments

- 2026-10-25, after the decision to make all-MiniLM-L6-v2 the default embedder (see ticket 03's comments): re-ran `run_experiment.py --embedder minilm --batch-size 32 --n 500` in the root environment, unmodified (transformers 4.57.6, sentence-transformers 5.7.0, toponymy 0.5.4), with `think: False` and `num_ctx: 16384`. Result: 3 cluster layers (27, 11 and 6 clusters), every one of the 44 clusters labeled by `gemma4:e4b-it-qat`, 0 parse failures in 38 calls, no re-clustering (spies counted 0 calls; Toponymy used the precomputed layers). Embedding 500 abstracts took 4 s; `Toponymy.fit` took 450 s, about 10 s per cluster, almost all of it in the LLM. Noise share was 37–40% at each layer. Example labels: "Deep Learning Applications in Audio Signal Processing and Speech Tasks", "Theoretical Analysis of Thompson Sampling and Multi-Armed Bandit Regret Bounds".
