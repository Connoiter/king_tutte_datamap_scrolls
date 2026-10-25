"""Ticket 03: do Gemma 4 (Ollama) and EmbeddingGemma 2 fit together on 16 GB?

Loads EmbeddingGemma 2 (sentence-transformers) and a Gemma 4 model (Ollama),
embeds a fixed-seed sample of arXiv ML abstracts, and asks Gemma 4 for short
completions while the embedder is loaded and working. A sampler thread
records, every 0.5 s: this process's memory, the Ollama processes' memory,
and system memory / swap / pressure. Results go to a JSON file.

Memory is read as macOS `phys_footprint` (what Activity Monitor calls
"Memory"; it includes Metal/GPU buffers, which plain RSS can miss) and RSS,
per process, so a concurrent unrelated job does not pollute the numbers.

Needs transformers>=5 and sentence-transformers>=6.1 (see the ticket's
Answer). Run, from the repo root, with an environment that has those, e.g.

    uv run --project <env-with-transformers-5> python \
        experiments/03-models-in-memory/measure.py --out results-e4b.json

Data (lmcinnes/arxiv_ml, CC0) is downloaded to the Hugging Face cache, never
into the repo.
"""

import argparse
import ctypes
import json
import os
import subprocess
import threading
import time
import urllib.request

# No account or token: make sure nothing implicit is used.
os.environ.pop("HF_TOKEN", None)
os.environ["HF_HUB_DISABLE_IMPLICIT_TOKEN"] = "1"

import psutil  # noqa: E402

from embedding_format import format_document  # noqa: E402

EMBEDDER_ID = "google/embeddinggemma-2"
DATASET_ID = "lmcinnes/arxiv_ml"
OLLAMA = "http://localhost:11434"
GIB = 1024**3


# --- memory sampling -------------------------------------------------------

class _RUsageInfoV2(ctypes.Structure):
    _fields_ = [("ri_uuid", ctypes.c_uint8 * 16)] + [
        (name, ctypes.c_uint64)
        for name in (
            "ri_user_time ri_system_time ri_pkg_idle_wkups ri_interrupt_wkups "
            "ri_pageins ri_wired_size ri_resident_size ri_phys_footprint "
            "ri_proc_start_abstime ri_proc_exit_abstime ri_child_user_time "
            "ri_child_system_time ri_child_pkg_idle_wkups ri_child_interrupt_wkups "
            "ri_child_pageins ri_child_elapsed_abstime ri_diskio_bytesread "
            "ri_diskio_byteswritten"
        ).split()
    ]


_libc = ctypes.CDLL("/usr/lib/libSystem.B.dylib")


def phys_footprint(pid: int) -> int | None:
    info = _RUsageInfoV2()
    if _libc.proc_pid_rusage(pid, 2, ctypes.byref(info)) != 0:
        return None
    return info.ri_phys_footprint


def ollama_pids() -> list[int]:
    pids = []
    for p in psutil.process_iter(["name", "cmdline"]):
        name = (p.info["name"] or "").lower()
        cmd = " ".join(p.info["cmdline"] or []).lower()
        # `ollama serve` plus its runner (`llama-server` or `ollama runner`).
        if "ollama" in name or "llama-server" in name or "ollama" in cmd.split(" ")[0]:
            pids.append(p.pid)
    return pids


def pressure_level() -> int | None:
    # 1 = normal, 2 = warn, 4 = critical
    try:
        out = subprocess.run(
            ["sysctl", "-n", "kern.memorystatus_vm_pressure_level"],
            capture_output=True, text=True, timeout=2,
        ).stdout.strip()
        return int(out)
    except Exception:
        return None


def sample(phase: str) -> dict:
    me = os.getpid()
    ollama = []
    for pid in ollama_pids():
        try:
            p = psutil.Process(pid)
            ollama.append({
                "pid": pid,
                "cmd": " ".join(p.cmdline()[:2]),
                "rss": p.memory_info().rss,
                "footprint": phys_footprint(pid),
            })
        except (psutil.Error, OSError):
            pass
    vm = psutil.virtual_memory()
    sw = psutil.swap_memory()
    return {
        "t": time.time(),
        "phase": phase,
        "self_rss": psutil.Process(me).memory_info().rss,
        "self_footprint": phys_footprint(me),
        "ollama": ollama,
        "ollama_footprint_total": sum(o["footprint"] or 0 for o in ollama),
        "ollama_rss_total": sum(o["rss"] for o in ollama),
        "sys_available": vm.available,
        "sys_used": vm.used,
        "sys_wired": getattr(vm, "wired", None),
        "swap_used": sw.used,
        "swap_sin": sw.sin,
        "swap_sout": sw.sout,
        "pressure": pressure_level(),
    }


class Sampler(threading.Thread):
    def __init__(self, interval=0.5):
        super().__init__(daemon=True)
        self.interval = interval
        self.phase = "start"
        self.samples: list[dict] = []
        self._halt = threading.Event()

    def run(self):
        while not self._halt.is_set():
            self.samples.append(sample(self.phase))
            self._halt.wait(self.interval)

    def stop(self):
        self._halt.set()
        self.join()


# --- data ------------------------------------------------------------------

def load_sample(n: int, seed: int) -> list[dict]:
    import pyarrow.parquet as pq
    from huggingface_hub import hf_hub_download, list_repo_files
    import numpy as np

    shard = sorted(f for f in list_repo_files(DATASET_ID, repo_type="dataset")
                   if f.endswith(".parquet"))[0]
    path = hf_hub_download(DATASET_ID, shard, repo_type="dataset")
    table = pq.read_table(path, columns=["arxiv_id", "title", "abstract"])
    idx = np.random.default_rng(seed).choice(table.num_rows, size=n, replace=False)
    rows = table.take(sorted(idx)).to_pylist()
    for r in rows:
        r["title"] = " ".join((r["title"] or "").split())
        r["abstract"] = " ".join((r["abstract"] or "").split())
    return rows


# --- ollama ----------------------------------------------------------------

def ollama_post(path: str, payload: dict, timeout=600) -> dict:
    req = urllib.request.Request(
        OLLAMA + path, data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read())


def ollama_ps() -> list[dict]:
    with urllib.request.urlopen(OLLAMA + "/api/ps", timeout=10) as r:
        return json.loads(r.read())["models"]


def ask(model: str, prompt: str, think: bool) -> dict:
    t = time.perf_counter()
    r = ollama_post("/api/chat", {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "stream": False,
        "think": think,
        "keep_alive": "10m",
        "options": {"num_predict": 128, "temperature": 0.2},
    })
    wall = time.perf_counter() - t
    return {
        "prompt": prompt[:80],
        "wall_s": wall,
        "load_s": r.get("load_duration", 0) / 1e9,
        "prompt_tokens": r.get("prompt_eval_count"),
        "gen_tokens": r.get("eval_count"),
        "gen_tok_per_s": (r.get("eval_count") or 0) / max(r.get("eval_duration", 1) / 1e9, 1e-9),
        "answer": r["message"]["content"][:200],
    }


def naming_prompts(rows: list[dict], k: int) -> list[str]:
    """Short cluster-naming style prompts, similar in spirit to Toponymy's."""
    prompts = []
    for i in range(k):
        titles = "\n".join("- " + r["title"] for r in rows[i * 8:(i + 1) * 8])
        prompts.append(
            "Here are titles of machine learning papers from one cluster:\n"
            f"{titles}\n"
            "Give a short (2-5 word) name for the topic of this cluster. "
            "Answer with the name only."
        )
    return prompts


# --- main ------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=400)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--model", default="gemma4:e4b-it-qat")
    ap.add_argument("--device", default="mps")
    ap.add_argument("--dtype", default="bfloat16", choices=["bfloat16", "float32"])
    ap.add_argument("--batch-size", type=int, default=16)
    ap.add_argument("--asks", type=int, default=6)
    ap.add_argument("--think", action="store_true")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    result: dict = {"args": vars(args), "timings": {}}
    sampler = Sampler()
    sampler.start()

    # Unload any running Ollama model so the baseline is clean.
    for m in ollama_ps():
        ollama_post("/api/generate", {"model": m["name"], "keep_alive": 0})
    time.sleep(2)

    sampler.phase = "data"
    rows = load_sample(args.n, args.seed)
    docs = [format_document(r["abstract"], r["title"]) for r in rows]
    result["n_docs"] = len(docs)

    sampler.phase = "load_embedder"
    import torch
    import transformers
    import sentence_transformers
    from sentence_transformers import SentenceTransformer

    result["versions"] = {
        "torch": torch.__version__,
        "transformers": transformers.__version__,
        "sentence_transformers": sentence_transformers.__version__,
    }
    t = time.perf_counter()
    embedder = SentenceTransformer(
        EMBEDDER_ID,
        device=args.device,
        model_kwargs={"dtype": getattr(torch, args.dtype)},
        config_kwargs={"vision_config": None, "audio_config": None},
    )
    result["timings"]["embedder_load_s"] = time.perf_counter() - t
    result["embedder_params_M"] = sum(p.numel() for p in embedder.parameters()) / 1e6
    # The checkpoint leaves max_seq_length unbounded (~1e30); cap it at the
    # model's 8K context so long documents are embedded whole, not overflowed.
    result["embedder_default_max_seq_length"] = embedder.max_seq_length
    embedder.max_seq_length = 8192

    # Warm-up, then embedding alone.
    embedder.encode(docs[:args.batch_size], batch_size=args.batch_size)
    sampler.phase = "embed_alone"
    t = time.perf_counter()
    emb = embedder.encode(docs, batch_size=args.batch_size, normalize_embeddings=True)
    dt = time.perf_counter() - t
    result["timings"]["embed_alone_s"] = dt
    result["docs_per_s_alone"] = len(docs) / dt
    result["embedding_shape"] = list(emb.shape)
    result["embedding_finite"] = bool(__import__("numpy").isfinite(emb).all())

    # Distinct prompts per phase, so Ollama's prompt cache cannot flatter
    # the concurrent timings.
    prompts = naming_prompts(rows, 3 + args.asks)

    sampler.phase = "load_gemma"
    first = ask(args.model, "Reply with the single word: ready.", args.think)
    result["gemma_cold"] = first
    result["ollama_ps"] = ollama_ps()

    sampler.phase = "gemma_alone"
    result["gemma_alone"] = [ask(args.model, p, args.think) for p in prompts[:3]]

    # Both at once: embed (repeatedly, in a thread) while Gemma answers.
    sampler.phase = "both"
    stop = threading.Event()
    counts = {"docs": 0, "secs": 0.0}

    def embed_loop():
        while not stop.is_set():
            t0 = time.perf_counter()
            embedder.encode(docs, batch_size=args.batch_size)
            counts["docs"] += len(docs)
            counts["secs"] += time.perf_counter() - t0

    th = threading.Thread(target=embed_loop)
    th.start()
    time.sleep(1)
    result["mps_driver_allocated_GiB_during_both"] = (
        torch.mps.driver_allocated_memory() / GIB if args.device == "mps" else None)
    result["gemma_concurrent"] = [ask(args.model, p, args.think) for p in prompts[3:]]
    # Keep both busy until at least one full embedding pass has finished.
    # (Repeated prompt, so these are prompt-cache hits; kept apart.)
    result["gemma_concurrent_filler"] = []
    while counts["docs"] == 0:
        result["gemma_concurrent_filler"].append(ask(args.model, prompts[3], args.think))
    stop.set()
    th.join()
    result["docs_per_s_concurrent"] = counts["docs"] / max(counts["secs"], 1e-9)
    result["concurrent_docs"] = counts["docs"]
    result["ollama_ps_after"] = ollama_ps()

    sampler.phase = "end"
    time.sleep(1)
    sampler.stop()
    s = sampler.samples
    peak = lambda key, ph=None: max((x[key] or 0) for x in s if ph is None or x["phase"] in ph)
    result["peak"] = {
        "self_footprint_GiB": peak("self_footprint") / GIB,
        "self_rss_GiB": peak("self_rss") / GIB,
        "ollama_footprint_GiB": peak("ollama_footprint_total") / GIB,
        "ollama_rss_GiB": peak("ollama_rss_total") / GIB,
        "combined_footprint_both_GiB": max(
            ((x["self_footprint"] or 0) + x["ollama_footprint_total"]) for x in s
            if x["phase"] == "both") / GIB,
        "sys_used_GiB": peak("sys_used") / GIB,
        "min_available_GiB": min(x["sys_available"] for x in s) / GIB,
        "swap_used_start_GiB": s[0]["swap_used"] / GIB,
        "swap_used_max_GiB": peak("swap_used") / GIB,
        "swapouts_during_run_GiB": (s[-1]["swap_sout"] - s[0]["swap_sout"]) / GIB,
        "max_pressure_level": peak("pressure"),
        "baseline_available_GiB": s[0]["sys_available"] / GIB,
        "baseline_pressure_level": s[0]["pressure"],
        "pressure_by_phase": {
            ph: sorted({x["pressure"] for x in s if x["phase"] == ph})
            for ph in dict.fromkeys(x["phase"] for x in s)},
    }
    result["samples"] = s
    with open(args.out, "w") as f:
        json.dump(result, f, indent=1, default=str)
    summary = {k: v for k, v in result.items() if k != "samples"}
    print(json.dumps(summary, indent=1, default=str))


if __name__ == "__main__":
    main()
