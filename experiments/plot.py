# The code generates runtime comparison plots for vertex cover and graph coloring.
import csv
from pathlib import Path
import matplotlib.pyplot as plt

def read_results(filename):
    # the code reads the CSV file and convert numeric columns.
    with open(filename, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    for row in rows:
        row["n"] = int(row["n"])
        row["m"] = int(row["m"])
        row["time_ms"] = float(row["time_ms"])
    return rows

def make_plot(rows, problem):
    # The code compares measured runtime with scaled theoretical complexity
    plt.figure(figsize=(7, 4.5))

    colors = {"vertex_cover": {"basic": "blue", "randomized": "red"}, "coloring": {"basic": "green", "dsatur": "purple"},}
    relevant = [r for r in rows if r["problem"] == problem]
    for name in sorted({r["algorithm"] for r in relevant}):
        points = sorted(
            (r for r in relevant if r["algorithm"] == name),
            key=lambda r: r["n"])
        x = [r["n"] for r in points]
        y = [r["time_ms"] for r in points]
        plt.plot(x, y, color=colors[problem][name], linewidth=2, label=name)
        
        # Theoretical growth O(E) for vertex cover, O(V + E) for basic coloring, and O(V^2 + E) for DSATUR.
        if problem == "vertex_cover":
            if name != "basic":
                continue
            growth = [r["m"] for r in points]
            label = "O(E) (scaled)"
            style = "--"
        elif name == "basic":
            growth = [r["n"] + r["m"] for r in points]
            label = "O(V + E) (scaled)"
            style = "--"
        else:
            growth = [r["n"] ** 2 + r["m"] for r in points]
            label = "O(V² + E) (scaled)"
            style = ":"
        # The code scales reference growth using T_ref = T0 * growth / growth0.
        reference = [y[0] * value / growth[0] for value in growth]
        plt.plot(x, reference, linestyle=style, color="gray", linewidth=2, label=label)

    plt.xlabel("Number of vertices (BHOSLIB/FRB)")
    plt.ylabel("Mean runtime (ms)")
    plt.title(f"{problem.replace('_', ' ').title()} - Runtime")
    plt.legend()
    plt.grid(True, alpha=0.25)
    plt.tight_layout()
    
    # It saves the plot as a PNG file.
    Path("results/figures").mkdir(parents=True, exist_ok=True)
    filename = f"results/figures/{problem}_time_ms.png"
    plt.savefig(filename, dpi=160)
    plt.close()
    print(f"Saved {filename}")

def main():
    # the code generates the two runtime plots
    rows = read_results("results/summary.csv")
    for problem in ("vertex_cover", "coloring"):
        make_plot(rows, problem)

if __name__ == "__main__":
    main()
