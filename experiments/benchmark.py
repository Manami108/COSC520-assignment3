"""Benchmark four graph algorithms using official BHOSLIB/FRB instances."""

import csv
import tracemalloc
from pathlib import Path
from statistics import median
from time import perf_counter

from algorithms.graph_coloring import (
    basic_graph_coloring, dsatur_coloring, valid_coloring, number_of_colors,
)
from algorithms.vertex_cover import (
    basic_vertex_cover, randomized_vertex_cover, valid_vertex_cover,
)
from experiments.dataset import load_graph


METHODS = [
    ("vertex_cover", "basic", basic_vertex_cover),
    ("vertex_cover", "randomized", randomized_vertex_cover),
    ("coloring", "basic", basic_graph_coloring),
    ("coloring", "dsatur", dsatur_coloring),
]

# One official graph instance from each of five FRB benchmark sizes.
# The integer is both the maximum independent-set size in MIS instances
# and the optimal number of colors in corresponding CLQ instances.
FRB_CASES = [
    ("frb30-15-1", 30),
    ("frb35-17-1", 35),
    ("frb40-19-1", 40),
    ("frb45-21-1", 45),
    ("frb50-23-1", 50),
]


def benchmark(graph, dataset, problem, optimum, repeats, seed):
    """Measure runtime, solution size, and peak traced Python memory.

    Graph loading and correctness checking are excluded from measurements.
    Memory is measured in a separate run to avoid slowing timed runs.
    """
    rows = []
    for task, name, function in METHODS:
        if task != problem:
            continue

        tracemalloc.start()
        try:
            if name == "randomized":
                memory_result = function(graph, seed=seed)
            else:
                memory_result = function(graph)
            peak_mb = tracemalloc.get_traced_memory()[1] / (1024 * 1024)
        finally:
            tracemalloc.stop()
        del memory_result

        for trial in range(repeats):
            start = perf_counter()
            if name == "randomized":
                result = function(graph, seed=seed + trial)
            else:
                result = function(graph)
            elapsed_ms = (perf_counter() - start) * 1000

            if problem == "vertex_cover":
                assert valid_vertex_cover(graph, result)
                solution_size = len(result)
            else:
                assert valid_coloring(graph, result)
                solution_size = number_of_colors(result)

            rows.append({
                "dataset": dataset, "n": graph.n, "m": len(graph.edges),
                "problem": problem, "algorithm": name, "repeat": trial + 1,
                "time_ms": round(elapsed_ms, 6),
                "solution_size": solution_size,
                "optimum": optimum,
                "peak_memory_mb": round(peak_mb, 6),
            })
    return rows


def save_csv(rows, filename):
    """Write benchmark results to a CSV file."""
    Path(filename).parent.mkdir(parents=True, exist_ok=True)
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def summarize(rows):
    """Calculate median time and solution size for each graph and algorithm."""
    groups = {}
    for row in rows:
        key = (row["dataset"], row["problem"], row["algorithm"])
        groups.setdefault(key, []).append(row)

    summary = []
    for (dataset, problem, algorithm), group in groups.items():
        first = group[0]
        summary.append({
            "dataset": dataset, "n": first["n"], "m": first["m"],
            "problem": problem, "algorithm": algorithm,
            "time_ms": round(median(r["time_ms"] for r in group), 6),
            "solution_size": median(r["solution_size"] for r in group),
            "optimum": first["optimum"],
            "peak_memory_mb": first["peak_memory_mb"],
        })
    return sorted(summary, key=lambda r: (r["problem"], r["n"], r["algorithm"]))


def main():
    """Run the benchmark only on official FRB graphs in the data folder."""
    repeats = 3
    seed = 42

    # Each graph family provides an MIS file for vertex cover and a CLQ
    # file (its complement) for coloring.
    paths = [(case, k, problem, Path("data") / f"{case}.{extension}")
             for case, k in FRB_CASES
             for problem, extension in (("vertex_cover", "mis"), ("coloring", "clq"))]
    missing = [str(path) for _, _, _, path in paths if not path.is_file()]
    if missing:
        raise FileNotFoundError(
            "Download the missing official FRB datasets (see README.md):\n" +
            "\n".join(missing)
        )

    rows = []
    for _, k, problem, path in paths:
        graph = load_graph(path)
        optimum = graph.n - k if problem == "vertex_cover" else k
        print(f"Benchmarking {path.name}: {graph.n} vertices, {len(graph.edges)} edges")
        rows.extend(benchmark(graph, path.name, problem, optimum, repeats, seed))

    save_csv(rows, "results/benchmark.csv")
    summary = summarize(rows)
    save_csv(summary, "results/summary.csv")

    for row in summary:
        print(f"{row['dataset']:20} {row['algorithm']:12} "
              f"{row['time_ms']:.3f} ms   size={row['solution_size']:g} "
              f"optimal={row['optimum']}   memory={row['peak_memory_mb']:.3f} MB")
    print("Saved results/benchmark.csv and results/summary.csv")


if __name__ == "__main__":
    main()
