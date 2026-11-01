"""Plot runtime, solution quality, and peak memory on FRB benchmark graphs."""

import csv
from pathlib import Path
import matplotlib.pyplot as plt


def read_results(filename):
    """Read the benchmark summary CSV and convert numerical values."""
    with open(filename, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    for row in rows:
        row["n"] = int(row["n"])
        for column in ("time_ms", "solution_size", "peak_memory_mb", "optimum"):
            row[column] = float(row[column])
    return rows


def make_plot(rows, problem, metric):
    """Create one graph for two algorithms solving the same problem."""
    plt.figure(figsize=(7, 4.5))
    relevant = [r for r in rows if r["problem"] == problem]
    for name in sorted({r["algorithm"] for r in relevant}):
        points = sorted((r for r in relevant if r["algorithm"] == name),
                        key=lambda r: r["n"])
        plt.plot([r["n"] for r in points], [r[metric] for r in points],
                 marker="o", label=name)

    if metric == "solution_size":
        # The FRB collection documents the exact optimum for these instances.
        optimal = sorted({(r["n"], r["optimum"]) for r in relevant})
        plt.plot([n for n, _ in optimal], [v for _, v in optimal],
                 linestyle="--", label="optimal")

    plt.xlabel("Number of vertices (BHOSLIB/FRB)")
    if metric == "time_ms":
        plt.ylabel("Median runtime (ms)")
    elif metric == "peak_memory_mb":
        plt.ylabel("Peak traced Python memory (MB)")
    elif problem == "vertex_cover":
        plt.ylabel("Vertices in cover")
    else:
        plt.ylabel("Number of colors")
    plt.title(f"{problem.replace('_', ' ').title()} - {metric.replace('_', ' ')}")
    plt.legend()
    plt.grid(alpha=0.25)
    plt.tight_layout()
    Path("results/figures").mkdir(parents=True, exist_ok=True)
    filename = f"results/figures/{problem}_{metric}.png"
    plt.savefig(filename, dpi=160)
    plt.close()
    print(f"Saved {filename}")


def main():
    """Generate six comparison figures from the official FRB results."""
    rows = read_results("results/summary.csv")
    for problem in ("vertex_cover", "coloring"):
        for metric in ("time_ms", "solution_size", "peak_memory_mb"):
            make_plot(rows, problem, metric)


if __name__ == "__main__":
    main()
