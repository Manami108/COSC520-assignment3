"""Graph representation, DIMACS reader, and synthetic graph generator."""

import gzip
import random
from pathlib import Path


class Graph:
    def __init__(self, n):
        """Input: number of vertices. Output: empty undirected graph."""
        if n < 0:
            raise ValueError("Vertex count cannot be negative")
        self.n = n
        self.adj = [set() for _ in range(n)]
        self.edges = []

    def add_edge(self, u, v):
        """Input: two vertex IDs. Output: None; add one undirected edge."""
        if not (0 <= u < self.n and 0 <= v < self.n) or u == v:
            raise ValueError(f"Invalid edge: ({u}, {v})")
        if v not in self.adj[u]:
            self.adj[u].add(v)
            self.adj[v].add(u)
            self.edges.append((u, v))


def load_graph(filename):
    """Input: DIMACS .col/.clq file (optionally .gz). Output: Graph.

    Convert the 1-based vertex numbers in DIMACS files to 0-based IDs.
    """
    filename = Path(filename)
    opener = gzip.open if filename.suffix == ".gz" else open
    graph = None
    expected_edges = None

    with opener(filename, "rt", encoding="utf-8") as f:
        for line in f:
            parts = line.split()
            if not parts or parts[0] in ("c", "%"):
                continue
            if parts[0] == "p":
                if graph is not None or len(parts) != 4 or parts[1] not in ("edge", "edges", "col"):
                    raise ValueError("Invalid DIMACS header")
                graph = Graph(int(parts[2]))
                expected_edges = int(parts[3])
            elif parts[0] == "e" and graph is not None and len(parts) == 3:
                graph.add_edge(int(parts[1]) - 1, int(parts[2]) - 1)
            else:
                raise ValueError(f"Invalid DIMACS line: {line.strip()}")

    if graph is None or len(graph.edges) != expected_edges:
        raise ValueError("Missing header or incorrect edge count")
    return graph


def random_graph(n, probability=0.05, seed=42):
    """Input: size, edge probability, seed. Output: random undirected graph."""
    if not 0 <= probability <= 1:
        raise ValueError("Probability must be between 0 and 1")
    rng = random.Random(seed)
    graph = Graph(n)
    for u in range(n):
        for v in range(u + 1, n):
            if rng.random() < probability:
                graph.add_edge(u, v)
    return graph
