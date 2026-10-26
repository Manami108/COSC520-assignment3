"""Measure the four algorithms on generated graphs or DIMACS files.

Examples:
    python -m experiments.benchmark
    python -m experiments.benchmark --files data/example.col
"""

import argparse
import csv
from pathlib import Path
from statistics import median
from time import perf_counter

from algorithms.graph_coloring import (
    basic_graph_coloring, degree_ordered_coloring, valid_coloring,
    number_of_colors,
)
from algorithms.vertex_cover import (
    basic_vertex_cover, randomized_vertex_cover, valid_vertex_cover,
)
from experiments.dataset import load_graph, random_graph


METHODS = [
    ("vertex_cover", "basic", basic_vertex_cover),
    ("vertex_cover", "randomized", randomized_vertex_cover),
    ("coloring", "basic", basic_graph_coloring),
    ("coloring", "degree_ordered", degree_ordered_coloring),
]


def benchmark(graph, dataset, repeats=3, seed=42):
    """Input: graph, name, repeat count, seed. Output: timing rows.

    Loading and validation are excluded from the measured execution time.
    """
    rows = []
    for problem, name, function in METHODS:
        for trial in range(repeats):
            start = perf_counter()
            if name == "randomized":
                result = function(graph, seed=seed + trial)
            else:
                result = function(graph)
            time_ms = (perf_counter() - start) * 1000

            if problem == "vertex_cover":
                assert valid_vertex_cover(graph, result)
                size = len(result)
            else:
                assert valid_coloring(graph, result)
                size = number_of_colors(result)

            rows.append({
                "dataset": dataset, "n": graph.n, "m": len(graph.edges),
                "problem": problem, "algorithm": name, "repeat": trial + 1,
                "time_ms": round(time_ms, 6), "solution_size": size,
            })
    return rows


def save_csv(rows, filename):
    """Input: result dictionaries and file path. Output: written CSV."""
    Path(filename).parent.mkdir(exist_ok=True, parents=True)
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def summarize(rows):
    """Input: benchmark rows. Output: medians for each dataset and method."""
    groups = {}
    for row in rows:
        key = (row["dataset"], row["n"], row["m"],
               row["problem"], row["algorithm"])
        groups.setdefault(key, []).append(row)

    summary = []
    for (dataset, n, m, problem, algorithm), group in groups.items():
        summary.append({
            "dataset": dataset, "n": n, "m": m,
            "problem": problem, "algorithm": algorithm,
            "time_ms": round(median(row["time_ms"] for row in group), 6),
            "solution_size": median(row["solution_size"] for row in group),
        })
    return sorted(summary, key=lambda row: (row["n"], row["dataset"],
                                            row["problem"], row["algorithm"]))


def main():
    """Input: command-line settings. Output: raw and summary CSV files."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--files", nargs="+", help="DIMACS .col or .clq graphs")
    parser.add_argument("--sizes", default="100,200,400,800")
    parser.add_argument("--probability", type=float, default=0.05)
    parser.add_argument("--repeats", type=int, default=3)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()
    if args.repeats < 1:
        parser.error("--repeats must be positive")

    datasets = []
    if args.files:
        for filename in args.files:
            datasets.append((Path(filename).name, load_graph(filename)))
    else:
        for n in (int(x.strip()) for x in args.sizes.split(",")):
            datasets.append((f"random_{n}", random_graph(n, args.probability, args.seed)))

    rows = []
    for name, graph in datasets:
        print(f"Benchmarking {name}: {graph.n} vertices, {len(graph.edges)} edges")
        rows.extend(benchmark(graph, name, args.repeats, args.seed))

    save_csv(rows, "results/benchmark.csv")
    summary = summarize(rows)
    save_csv(summary, "results/summary.csv")
    for row in summary:
        print(f"{row['dataset']:20} {row['problem']:12} {row['algorithm']:14} "
              f"{row['time_ms']:.4f} ms   size={row['solution_size']:g}")
    print("Saved results/benchmark.csv and results/summary.csv")


if __name__ == "__main__":
    main()
