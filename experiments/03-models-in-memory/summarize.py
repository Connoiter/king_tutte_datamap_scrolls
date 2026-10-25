"""Print a one-row-per-run summary of measure.py result files."""

import json
import statistics
import sys


def med(xs):
    return round(statistics.median(xs), 2) if xs else None


def main(paths):
    for path in paths:
        r = json.load(open(path))
        a, p = r["args"], r["peak"]
        alone = [x["wall_s"] for x in r["gemma_alone"]]
        conc = [x["wall_s"] for x in r["gemma_concurrent"]]
        print(f"== {path}")
        print(f"  model={a['model']} dtype={a['dtype']} batch={a['batch_size']} n={r['n_docs']}"
              f"  versions={r['versions']}")
        print(f"  embed docs/s alone={r['docs_per_s_alone']:.1f}"
              f" concurrent={r['docs_per_s_concurrent']:.1f}")
        print(f"  gemma cold={r['gemma_cold']['wall_s']:.1f}s (load {r['gemma_cold']['load_s']:.1f}s)"
              f" median alone={med(alone)}s concurrent={med(conc)}s"
              f" tok/s alone={med([x['gen_tok_per_s'] for x in r['gemma_alone']])}"
              f" concurrent={med([x['gen_tok_per_s'] for x in r['gemma_concurrent']])}")
        print(f"  ollama ps size={r['ollama_ps'][0]['size'] / 2**30:.2f} GiB"
              f" ctx={r['ollama_ps'][0]['context_length']}")
        print("  peak: " + ", ".join(
            f"{k}={v:.2f}" if isinstance(v, float) else f"{k}={v}"
            for k, v in p.items() if k != "pressure_by_phase"))
        print(f"  pressure by phase: {p.get('pressure_by_phase')}")


if __name__ == "__main__":
    main(sys.argv[1:])
