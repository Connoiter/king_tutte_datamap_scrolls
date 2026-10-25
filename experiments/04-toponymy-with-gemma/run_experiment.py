"""Experiment 04: Toponymy labels precomputed clusters with Gemma 4 via Ollama.

Pipeline on a small fixed-seed sample of lmcinnes/arxiv_ml (CC0) abstracts:

1. Embed `title: <title> | text: <abstract>` with EmbeddingGemma 2 (bf16, MPS),
   or all-MiniLM-L6-v2 with --embedder minilm.
2. UMAP to 2D with a fixed random_state.
3. ToponymyClusterer on the 2D map -> cluster layers.
4. Convert the layers to the schema's cluster tree (points.cluster + clusters
   rows with parent pointers) and back (cluster_tree.py), and wrap the result in
   PrecomputedClusterer (fit/fit_predict raise).
5. Toponymy.fit with OllamaNamer(model=gemma4:e4b-it-qat) and the embedder as
   the text embedding model, while spying on every clustering entry point.

A small logging proxy sits between litellm and Ollama so the exact request
bodies (think, format, options) and raw responses are recorded.

Run from the repo root (see the ticket's Answer for the environment):
    uv run --project <env> python experiments/04-toponymy-with-gemma/run_experiment.py \
        --out <dir>
"""

from __future__ import annotations

import argparse
import http.server
import json
import os
import re
import sys
import threading
import time
import urllib.request
from pathlib import Path

os.environ.pop("HF_TOKEN", None)  # EmbeddingGemma 2 is ungated; send no token
os.environ["HF_HUB_DISABLE_IMPLICIT_TOKEN"] = "1"
os.environ["LITELLM_LOCAL_MODEL_COST_MAP"] = "True"  # no network fetch at import
os.environ["TOKENIZERS_PARALLELISM"] = "false"

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent / "03-models-in-memory"))

DATASET_ID = "lmcinnes/arxiv_ml"
OLLAMA = "http://localhost:11434"


# --- data --------------------------------------------------------------------

def load_sample(n: int, seed: int) -> list[dict]:
    """Same sampling as experiment 03: first parquet shard, numpy default_rng(seed)."""
    import pyarrow.parquet as pq
    from huggingface_hub import hf_hub_download, list_repo_files

    shard = sorted(
        f for f in list_repo_files(DATASET_ID, repo_type="dataset") if f.endswith(".parquet")
    )[0]
    path = hf_hub_download(DATASET_ID, shard, repo_type="dataset")
    table = pq.read_table(path, columns=["arxiv_id", "title", "abstract"])
    idx = np.random.default_rng(seed).choice(table.num_rows, size=n, replace=False)
    rows = table.take(sorted(idx)).to_pylist()
    for r in rows:
        r["title"] = " ".join((r["title"] or "").split())
        r["abstract"] = " ".join((r["abstract"] or "").split())
    return rows


# --- embedder ----------------------------------------------------------------

def load_embedder(kind: str):
    from sentence_transformers import SentenceTransformer

    if kind == "gemma":
        import torch

        model = SentenceTransformer(
            "google/embeddinggemma-2",
            device="mps",
            model_kwargs={"dtype": torch.bfloat16},
            config_kwargs={"vision_config": None, "audio_config": None},
        )
        model.max_seq_length = 8192
        return model
    return SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2", device="mps")


class SmallBatchEmbedder:
    """Toponymy calls `.encode(texts, show_progress_bar=...)`; keep batches small (memory)."""

    def __init__(self, model, batch_size: int):
        self.model = model
        self.batch_size = batch_size
        self.calls: list[int] = []
        self.seconds = 0.0

    def encode(self, texts, show_progress_bar=None, **kwargs):
        start = time.perf_counter()
        self.calls.append(len(texts))
        kwargs.setdefault("batch_size", self.batch_size)
        kwargs.setdefault("normalize_embeddings", True)
        out = self.model.encode(texts, show_progress_bar=False, **kwargs)
        self.seconds += time.perf_counter() - start
        return out


# --- logging proxy between litellm and Ollama -------------------------------

class Exchange(dict):
    pass


def start_proxy(port: int, log: list[Exchange]):
    class Handler(http.server.BaseHTTPRequestHandler):
        def _forward(self, method: str):
            length = int(self.headers.get("Content-Length") or 0)
            body = self.rfile.read(length) if length else None
            start = time.perf_counter()
            req = urllib.request.Request(
                OLLAMA + self.path,
                data=body,
                method=method,
                headers={"Content-Type": self.headers.get("Content-Type", "application/json")},
            )
            try:
                with urllib.request.urlopen(req, timeout=600) as resp:
                    status, payload = resp.status, resp.read()
                    ctype = resp.headers.get("Content-Type", "application/json")
            except urllib.error.HTTPError as e:
                status, payload, ctype = e.code, e.read(), "application/json"
            log.append(
                Exchange(
                    method=method,
                    path=self.path,
                    request=body.decode() if body else None,
                    status=status,
                    response=payload.decode(errors="replace"),
                    seconds=time.perf_counter() - start,
                )
            )
            self.send_response(status)
            self.send_header("Content-Type", ctype)
            self.send_header("Content-Length", str(len(payload)))
            self.end_headers()
            self.wfile.write(payload)

        def do_POST(self):
            self._forward("POST")

        def do_GET(self):
            self._forward("GET")

        def log_message(self, *args):
            pass

    server = http.server.ThreadingHTTPServer(("127.0.0.1", port), Handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return server


# --- main ----------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=300)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--model", default="gemma4:e4b-it-qat")
    ap.add_argument("--embedder", default="gemma", choices=["gemma", "minilm"])
    ap.add_argument("--batch-size", type=int, default=4)
    ap.add_argument("--proxy-port", type=int, default=11435)
    ap.add_argument("--min-clusters", type=int, default=2)
    ap.add_argument("--base-min-cluster-size", type=int, default=5)
    ap.add_argument(
        "--think",
        default="off",
        choices=["off", "default"],
        help="off: provider_kwargs={'think': False}; default: what OllamaNamer sends on its own",
    )
    ap.add_argument("--num-ctx", type=int, default=16384, help="0: leave Ollama's default")
    ap.add_argument("--cluster-only", action="store_true", help="stop before Toponymy.fit")
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    results: dict = {"args": {k: str(v) for k, v in vars(args).items()}, "timings": {}}
    t = results["timings"]

    import sentence_transformers
    import toponymy
    import transformers

    results["versions"] = {
        "transformers": transformers.__version__,
        "sentence_transformers": sentence_transformers.__version__,
        "toponymy": getattr(toponymy, "__version__", "?"),
    }
    print("versions", results["versions"], flush=True)

    rows = load_sample(args.n, args.seed)
    from embedding_format import format_document

    docs = [format_document(r["abstract"], title=r["title"]) for r in rows]
    objects = [f"{r['title']}\n\n{r['abstract']}" for r in rows]

    start = time.perf_counter()
    model = load_embedder(args.embedder)
    t["embedder_load_s"] = time.perf_counter() - start
    cache = args.out / f"embeddings_{args.embedder}_{args.n}_{args.seed}.npy"
    start = time.perf_counter()
    if cache.exists():
        vectors = np.load(cache)
    else:
        vectors = model.encode(docs, batch_size=args.batch_size, normalize_embeddings=True)
        np.save(cache, vectors)
    t["embed_s"] = time.perf_counter() - start
    print("embedded", vectors.shape, f"{t['embed_s']:.1f}s", flush=True)

    import umap

    start = time.perf_counter()
    coords = umap.UMAP(n_components=2, metric="cosine", random_state=42).fit_transform(vectors)
    t["umap_s"] = time.perf_counter() - start

    import toponymy.clustering as tc
    from toponymy import Toponymy, ToponymyClusterer
    from toponymy.llm_wrappers import OllamaNamer
    from toponymy.templates import GET_TOPIC_CLUSTER_NAMES_REGEX, GET_TOPIC_NAME_REGEX

    from cluster_tree import layers_from_tree, tree_from_layers
    from precomputed_clusterer import PrecomputedClusterer

    start = time.perf_counter()
    clusterer = ToponymyClusterer(
        min_clusters=args.min_clusters,
        base_min_cluster_size=args.base_min_cluster_size,
        verbose=True,
    ).fit(coords, vectors)
    t["cluster_s"] = time.perf_counter() - start
    original = [layer.cluster_labels for layer in clusterer.cluster_layers_]
    results["clusters_per_layer"] = [int(x.max()) + 1 for x in original]
    results["noise_share_per_layer"] = [float(np.mean(x < 0)) for x in original]
    print("clusters per layer", results["clusters_per_layer"], flush=True)

    # Clusterer -> schema rows -> Labeler round trip.
    point_cluster, clusters = tree_from_layers(original)
    rebuilt = layers_from_tree(point_cluster, clusters)
    results["round_trip"] = {
        "points_changed_per_layer": [int(np.sum(a != b)) for a, b in zip(original, rebuilt)],
        "tree_equal_to_clusterer_tree": tc.build_cluster_tree(rebuilt) == clusterer.cluster_tree_,
        "parents_skipping_a_layer": sum(
            1
            for row in clusters
            if row["parent"] is not None
            and next(r for r in clusters if r["cluster"] == row["parent"])["layer"] != row["layer"] + 1
        ),
    }
    print("round trip", results["round_trip"], flush=True)
    (args.out / "clusters.json").write_text(
        json.dumps({"point_cluster": point_cluster.tolist(), "clusters": clusters})
    )
    if args.cluster_only:
        return

    # Spy on every way Toponymy could cluster again.
    spy_counts = {"build_raw_cluster_layers": 0, "ToponymyClusterer.fit": 0, "create_cluster_layers": 0}

    def spy(name, fn):
        def wrapper(*a, **k):
            spy_counts[name] += 1
            return fn(*a, **k)

        return wrapper

    tc.build_raw_cluster_layers = spy("build_raw_cluster_layers", tc.build_raw_cluster_layers)
    tc.create_cluster_layers = spy("create_cluster_layers", tc.create_cluster_layers)
    ToponymyClusterer.fit = spy("ToponymyClusterer.fit", ToponymyClusterer.fit)

    embedder = SmallBatchEmbedder(model, args.batch_size)
    pre = PrecomputedClusterer(point_cluster, clusters, vectors)

    debug_events: list[dict] = []

    def callback(payload):
        payload = dict(payload, t=time.perf_counter())
        raw = payload.get("raw_response")
        if raw is not None:
            regex = (
                GET_TOPIC_CLUSTER_NAMES_REGEX
                if payload.get("routine") == "generate_topic_cluster_names"
                else GET_TOPIC_NAME_REGEX
            )
            try:
                json.loads(re.findall(regex, raw, re.DOTALL)[0])
                payload["parsed"] = True
            except Exception as e:  # noqa: BLE001 - record any parse failure
                payload["parsed"] = False
                payload["parse_error"] = f"{type(e).__name__}: {e}"
        debug_events.append(payload)

    proxy_log: list[Exchange] = []
    proxy = start_proxy(args.proxy_port, proxy_log)
    provider_kwargs = {}
    if args.think == "off":
        provider_kwargs["think"] = False
    if args.num_ctx:
        provider_kwargs["num_ctx"] = args.num_ctx  # litellm forwards it into Ollama's options
    namer = OllamaNamer(
        model=args.model,
        api_base=f"http://127.0.0.1:{args.proxy_port}",
        callback=callback,
        # Gemma 4 thinks by default and OllamaNamer does not turn it off: the
        # 128-token budget goes on thinking and the answer comes back empty.
        # Ollama's default context here is 4,096 tokens and it silently
        # truncates longer prompts; disambiguation prompts run to ~10k tokens.
        provider_kwargs=provider_kwargs or None,
    )

    topic_model = Toponymy(
        llm_wrapper=namer,
        text_embedding_model=embedder,
        clusterer=pre,
        object_description="arXiv paper titles and abstracts",
        corpus_description="sample of arXiv machine learning papers",
        verbose=True,
    )
    start = time.perf_counter()
    error = None
    try:
        topic_model.fit(objects, vectors, coords)
    except Exception as e:  # noqa: BLE001 - record where it failed
        import traceback

        error = traceback.format_exc()
        print(error, flush=True)
    t["toponymy_fit_s"] = time.perf_counter() - start
    proxy.shutdown()

    results["error"] = error
    results["spy_counts"] = spy_counts
    results["fit_used_precomputed_layers"] = (
        error is None and topic_model.cluster_layers_ is pre.cluster_layers_
    )
    llm = [x for x in proxy_log if x["path"].startswith("/api/chat")]
    t["llm_http_s"] = sum(x["seconds"] for x in llm)
    t["embedder_in_fit_s"] = embedder.seconds
    results["embedder_calls_in_fit"] = embedder.calls
    results["proxy_paths"] = sorted({x["path"] for x in proxy_log})
    results["llm_calls"] = len(llm)
    results["llm_call_seconds"] = [round(x["seconds"], 3) for x in llm]

    # What litellm sent to Ollama, minus the message text.
    if llm:
        first = json.loads(llm[0]["request"])
        results["request_keys"] = {k: v for k, v in first.items() if k != "messages"}
        results["first_request"] = first
        stats = []
        for x in llm:
            try:
                r = json.loads(x["response"])
            except json.JSONDecodeError:
                continue
            stats.append(
                {
                    "prompt_chars": sum(
                        len(m["content"]) for m in json.loads(x["request"])["messages"]
                    ),
                    "seconds": round(x["seconds"], 2),
                    "prompt_eval_count": r.get("prompt_eval_count"),
                    "eval_count": r.get("eval_count"),
                    "has_thinking": bool((r.get("message") or {}).get("thinking")),
                    "done_reason": r.get("done_reason"),
                }
            )
        results["response_stats"] = stats
        results["first_response"] = json.loads(llm[0]["response"])

    by_routine: dict = {}
    for ev in debug_events:
        key = ev.get("routine") or "?"
        d = by_routine.setdefault(key, {"calls": 0, "parse_failures": 0, "http_errors": 0})
        if ev.get("event") == "llm_call_success":
            d["calls"] += 1
            d["parse_failures"] += 0 if ev.get("parsed") else 1
        else:
            d["http_errors"] += 1
    results["by_routine"] = by_routine
    results["parse_failure_examples"] = [
        {"routine": ev.get("routine"), "raw": ev.get("raw_response"), "error": ev.get("parse_error")}
        for ev in debug_events
        if ev.get("parsed") is False
    ][:10]
    results["error_examples"] = [ev for ev in debug_events if ev.get("event") != "llm_call_success"][:5]

    if error is None:
        names = topic_model.topic_names_
        results["topic_names"] = names
        results["empty_names_per_layer"] = [sum(1 for n in layer if not n) for layer in names]
        results["labels_per_layer_vs_clusters"] = [
            [len(layer_names), n] for layer_names, n in zip(names, results["clusters_per_layer"])
        ]
        n_clusters = sum(results["clusters_per_layer"])
        t["fit_s_per_cluster"] = t["toponymy_fit_s"] / n_clusters
        t["llm_s_per_cluster"] = t["llm_http_s"] / n_clusters

    (args.out / "debug_events.json").write_text(json.dumps(debug_events, default=str, indent=1))
    (args.out / "proxy_log.json").write_text(json.dumps(proxy_log, indent=1))
    (args.out / "results.json").write_text(json.dumps(results, indent=1, default=str))
    print(json.dumps({k: v for k, v in results.items() if k not in ("first_request",)}, indent=1, default=str)[:6000])


if __name__ == "__main__":
    main()
