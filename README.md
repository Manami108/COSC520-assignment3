# COSC 520 — Assignment 3

Compare two vertex cover algorithms (basic and randomized) and two greedy graph
coloring algorithms (natural order and largest-degree-first order).

## Project files

```text
algorithms/
  vertex_cover.py       Basic and randomized vertex cover
  graph_coloring.py     Basic and degree-ordered greedy coloring
data/
  example.col           Small example in DIMACS format
experiments/
  dataset.py            Graph class, DIMACS loader, and random graph generator
  benchmark.py          Measure runtime and solution size; save CSV files
  plot.py               Make four comparison plots
  demo.py               Run all four algorithms on the example graph
tests/
  tests.py              Six simple unit tests
requirements.txt
```

`__init__.py` files are included in `algorithms/` and `experiments/` for imports.
`results/` is created automatically by the benchmark and plotting scripts.

## Setup

Use Python 3.10+ and run the commands from this project directory:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Matplotlib is used only for the plots. No external libraries implement the algorithms.

## Run

```bash
python -m experiments.demo
python -m unittest discover -s tests -p 'tests.py' -v
python -m experiments.benchmark
python -m experiments.plot
```

For specific synthetic graph sizes:

```bash
python -m experiments.benchmark --sizes 100,300,500,1000 --repeats 5
```

For a DIMACS benchmark dataset (such as a BHOSLIB `.clq` file), put it in
`data/` and run:

```bash
python -m experiments.benchmark --files data/YOUR_FILE.clq --repeats 5
python -m experiments.plot
```

The benchmark generates `results/benchmark.csv` (individual runs) and
`results/summary.csv` (medians). The plot script makes four PNG files in
`results/figures/`. New benchmark runs overwrite the old results.

## Implementation notes

- The basic cover takes both endpoints of each still-uncovered edge; it is a
  2-approximation algorithm.
- The randomized cover takes one random endpoint per still-uncovered edge. It
  always covers every edge, but is not guaranteed to be a 2-approximation.
- Basic coloring visits vertices in numbered order.
- Degree-ordered coloring visits the highest-degree vertices first, with
  vertex ID breaking ties. Both assign the smallest available color.
- Graphs use 0-based vertex IDs in Python; DIMACS files use 1-based IDs.
- Runtime measurements do not include dataset loading or result validation.

## Before submitting

This is an AI-assisted starter implementation. The assignment asks you to make
and identify your own contributions rather than submit AI-generated algorithms
and tests as entirely your work. Review and modify the implementations, add
original test cases, and disclose AI assistance in the report. The report also
needs links to your GitHub repository and your actual benchmark dataset.
