# The code benchmark the basic and randomized vertex cover algorithms and the greedy and DSATUR graph coloring algorithms on FRB datasets.
# Each algorithm is evaluated by runtime, solution size, and peak memory.
import csv
import tracemalloc
from pathlib import Path
from statistics import mean, median, stdev
from time import perf_counter
from algorithms.graph_coloring import (basic_graph_coloring, dsatur_coloring, valid_coloring, number_of_colors,)
from algorithms.vertex_cover import (basic_vertex_cover, randomized_vertex_cover, valid_vertex_cover,)
from experiments.dataset import load_graph

METHODS = [
    ("vertex_cover", "basic", basic_vertex_cover),
    ("vertex_cover", "randomized", randomized_vertex_cover),
    ("coloring", "basic", basic_graph_coloring),
    ("coloring", "dsatur", dsatur_coloring),]

FRB_CASES = ["frb30-15-1", "frb35-17-1", "frb40-19-1", "frb45-21-1", "frb50-23-1", "frb53-24-1", "frb59-26-1",]

def benchmark(graph, dataset, repeats, seed):
    # Input: graph, dataset name, number of repetitions, and random seed
    # Output: list of benchmark results for all four algorithms
    # The code measures runtime, solution size, and peak Python memory for each method.
    # Memory is measured separately to avoid affecting timed executions.
    rows = []
    for problem, name, function in METHODS:
        tracemalloc.start()
        try:
            if name == "randomized":
                memory_result = function(graph, seed=seed)
            else:
                memory_result = function(graph)
            # Convert peak memory from bytes to MiB: bytes / (1024^2).
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
            # Runtime (ms) = (end time - start time) * 1000.
            elapsed_ms = (perf_counter() - start) * 1000
            # Solution size is the number of cover vertices or colors.
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
                "peak_memory_mb": round(peak_mb, 6),})
    return rows

def save_csv(rows, filename):
    # Input: list of result dictionaries and output filename
    # Output: CSV file containing the results
    # The code creates the output directory if it does not exist.
    Path(filename).parent.mkdir(parents=True, exist_ok=True)
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

def summarize(rows):
    # Input: list of benchmark results
    # Output: summary statistics grouped by dataset and algorithm
    # The code uses median runtime, mean solution size and sample standard deviation
    # Mean = sum(x) / k (k is the number of trials)
    # Sample SD = sqrt(sum((x - mean)^2) / (k - 1))
    groups = {}
    for row in rows:
        key = (row["dataset"], row["problem"], row["algorithm"])
        groups.setdefault(key, []).append(row)

    summary = []
    for (dataset, problem, algorithm), group in groups.items():
        first = group[0]
        times = [r["time_ms"] for r in group]
        sizes = [r["solution_size"] for r in group]
        summary.append({
            "dataset": dataset, "n": first["n"], "m": first["m"],
            "problem": problem, "algorithm": algorithm, "trials": len(group),
            "time_ms": round(median(times), 6),
            "time_std_ms": round(stdev(times), 6) if len(times) > 1 else 0,
            "solution_size": round(mean(sizes), 3),
            "solution_std": round(stdev(sizes), 3) if len(sizes) > 1 else 0,
            "peak_memory_mb": first["peak_memory_mb"], })
    return sorted(summary, key=lambda r: (r["problem"], r["n"], r["algorithm"]))

def main():
    # Input: none; uses the predefined FRB datasets
    # Output: benchmark.csv, summary.csv, and printed benchmark results
    # This block is to run all four algorithms three times on each FRB graph
    repeats = 3
    seed = 42
    rows = []
    for case in FRB_CASES:
        path = Path("data") / case / f"{case}.mtx"
        if not path.is_file():
            raise FileNotFoundError(f"Missing dataset: {path}")
        graph = load_graph(path)
        print(f"Benchmarking {case}: {graph.n} vertices, {len(graph.edges)} edges")
        rows.extend(benchmark(graph, case, repeats, seed))
        
    # This code save results and make summary
    save_csv(rows, "results/benchmark.csv")
    summary = summarize(rows)
    save_csv(summary, "results/summary.csv")
    
    # This is to display runtime, solution size, and peak memory for each method
    for row in summary:
        metric = "cover_vertices" if row["problem"] == "vertex_cover" else "colors"
        print(f"{row['dataset']:15} {row['problem']:12} "
            f"{row['algorithm']:12} "
            f"runs={row['trials']} "
            f"time={row['time_ms']:.3f} ms "
            f"{metric}={row['solution_size']:.2f} "
            f"peak_memory={row['peak_memory_mb']:.3f} MB")

if __name__ == "__main__":
    main()
