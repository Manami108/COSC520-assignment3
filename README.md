# COSC 520 Assignment 3

Hi! Welcome back to my GitHub repository, and Happy Halloween 🎃👻

This repository implements and compares two **Vertex Cover** algorithms (**Basic** and **Randomized**) and two **Graph Coloring** algorithms (**Basic Greedy** and **DSATUR**).

The algorithms are implemented in Python without using existing graph-algorithm implementations. The experiments compare execution time, solution size, and additional Python memory usage on seven BHOSLIB/FRB benchmark graphs.

## Repository Structure

```text
COSC520-assignment3/
│
├── algorithms/
│   ├── __init__.py
│   ├── vertex_cover.py
│   └── graph_coloring.py
│
├── experiments/
│   ├── __init__.py
│   ├── dataset.py
│   ├── benchmark.py
│   ├── plot.py
│   └── demo.py
│
├── tests/
│   ├── __init__.py
│   └── tests.py
│
├── data/
│   └── example.col
│
├── results/
├── requirements.txt
└── README.md
```

> [!IMPORTANT]
> The seven benchmark datasets must be downloaded separately and placed in the `data/` directory as described below.

## Implementations

The four graph algorithms are:

- **Basic Vertex Cover:** Selects both endpoints of an uncovered edge.
- **Randomized Vertex Cover:** Selects one randomly chosen endpoint of an uncovered edge. 
- **Basic Greedy Coloring:** Processes vertices in numerical order and assigns each vertex the smallest available color.
- **DSATUR Coloring:** Dynamically selects the uncolored vertex with the highest saturation degree, breaking ties by degree and vertex number, then assigns the smallest available color.

## Requirements and Running Instructions

This project uses Python 3.12 and `matplotlib` for visualizing benchmark results.

To install the required packages, I recommend creating a virtual environment first:

```bash
python3 -m venv .venv # Create a virtual environment

source .venv/bin/activate # Activate the environment (macOS/Linux)

python -m pip install -r requirements.txt # Install the required packages
```

Before running the benchmarks, download the seven BHOSLIB/FRB datasets and arrange them as shown in the **Dataset** section below. Run all commands from the repository's root directory.

To run the unit tests:

```bash
python -m unittest tests.tests -v
```

To run a basic demonstration of the four algorithms using `data/example.col`:

```bash
python -m experiments.demo
```

To run the benchmark experiments:

```bash
python -m experiments.benchmark
```

To generate the runtime figures after benchmarking:

```bash
python -m experiments.plot
```

## Generated Files

Running the experiments generates the following files:

- `results/benchmark.csv` — measurements from individual repetitions
- `results/summary.csv` — mean runtime, solution size, standard deviations, and peak traced memory
- `results/figures/vertex_cover_time_ms.png` — Basic versus Randomized Vertex Cover runtime
- `results/figures/coloring_time_ms.png` — Basic Greedy versus DSATUR Coloring runtime

The runtime figures also include gray, scaled theoretical complexity reference curves. 

## Dataset

The experiments use seven instances from the [BHOSLIB benchmark collection on Network Repository](https://networkrepository.com/bhoslib.php), as recommended for the assignment.

Download the ZIP file for each of these instances and extract the `.mtx` graph file:

| Dataset | Vertices | Edges |
|---|---:|---:|
| `frb30-15-1` | 450 | 83,198 |
| `frb35-17-1` | 595 | 148,859 |
| `frb40-19-1` | 760 | 247,106 |
| `frb45-21-1` | 945 | 386,854 |
| `frb50-23-1` | 1,150 | 580,603 |
| `frb53-24-1` | 1,272 | 714,129 |
| `frb59-26-1` | 1,534 | 1,049,256 |

Place the extracted files in the following folders. Keep the `.mtx` filenames unchanged:

```text
data/
├── example.col
├── frb30-15-1/frb30-15-1.mtx
├── frb35-17-1/frb35-17-1.mtx
├── frb40-19-1/frb40-19-1.mtx
├── frb45-21-1/frb45-21-1.mtx
├── frb50-23-1/frb50-23-1.mtx
├── frb53-24-1/frb53-24-1.mtx
└── frb59-26-1/frb59-26-1.mtx
```

The `readme.html` files bundled in the downloaded archives are not required to run the code. The small `example.col` is used only for tests and the demo, not for the main benchmark.

## Results

The benchmark compares runtime and solution quality on the same seven graphs. If you would rather skip the benchmarks (which is perfectly fine!), you can check the CSV results and generated figures in the `results/` directory.

### See you in the next project!
