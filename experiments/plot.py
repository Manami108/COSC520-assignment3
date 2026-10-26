"""Create runtime and solution-size plots from results/summary.csv."""

import csv
from pathlib import Path

import matplotlib.pyplot as plt


def read_results(filename):
    """Input: summary CSV path. Output: parsed benchmark rows."""
    with open(filename, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    for row in rows:
        row["n"] = int(row["n"])
        row["time_ms"] = float(row["time_ms"])
        row["solution_size"] = float(row["solution_size"])
    return rows


def make_plot(rows, problem, metric):
    """Input: summary rows, task and metric. Output: saved PNG figure."""
    plt.figure(figsize=(7, 4.5))
    names = sorted({r["algorithm"] for r in rows if r["problem"] == problem})
    for name in names:
        points = sorted((r for r in rows
                         if r["problem"] == problem and r["algorithm"] == name),
                        key=lambda r: r["n"])
        x = [r["n"] for r in points]
        y = [r[metric] for r in points]
        # Separate benchmark graphs can share n, so only join unique x values.
        if len(x) == len(set(x)):
            plt.plot(x, y, marker="o", label=name)
        else:
            plt.scatter(x, y, label=name)

    plt.xlabel("Number of vertices")
    if metric == "time_ms":
        plt.ylabel("Median runtime (ms)")
    elif problem == "vertex_cover":
        plt.ylabel("Number of selected vertices")
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
    """Input: results/summary.csv. Output: four comparison figures."""
    rows = read_results("results/summary.csv")
    for problem in ("vertex_cover", "coloring"):
        for metric in ("time_ms", "solution_size"):
            make_plot(rows, problem, metric)


if __name__ == "__main__":
    main()
