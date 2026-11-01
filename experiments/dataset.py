# The Graph class stores an undirected graph using adjacency sets and an edge list.
# Adjacency sets provide fast neighbor lookup and avoid duplicate edges.
from pathlib import Path

class Graph:
    def __init__(self, n):
        # Input: number of vertices
        # Output: empty undirected graph
        self.n = n
        self.adj = [set() for _ in range(n)]
        self.edges = []

    def add_edge(self, u, v):
        # Input: two vertex IDs
        # Output: None; add one undirected edge
        # It rejects invalid vertices and self-loops.
        if not (0 <= u < self.n and 0 <= v < self.n) or u == v:
            raise ValueError(f"Invalid edge: ({u}, {v})")
        if v not in self.adj[u]:
            self.adj[u].add(v)
            self.adj[v].add(u)
            self.edges.append((u, v))
            
def load_mtx(filename):
    # Input: Matrix Market file
    # Output: undirected graph
    # It reads a square adjacency matrix and converts entries into edges.
    with open(filename, "r", encoding="utf-8") as f:
        # The code is to skip the header and comments, and read matrix dimensions.
        for line in f:
            if not line.strip() or line.startswith("%"):
                continue
            n, columns, entries = map(int, line.split())
            if n != columns:
                raise ValueError("Expected a square adjacency matrix")
            graph = Graph(n)
            break
        else:
            raise ValueError("Missing Matrix Market dimensions")

        # Read edges and convert 1-based IDs to 0-based IDs.
        count = 0
        for line in f:
            if not line.strip() or line.startswith("%"):
                continue
            u, v = map(int, line.split()[:2])
            if u != v:
                graph.add_edge(u - 1, v - 1)
            count += 1
        if count != entries:
            raise ValueError("Incorrect number of entries")
    return graph


def load_graph(filename):
    # Input: Matrix Market (.mtx) or DIMACS graph file
    # Output: undirected graph
    # This block is to select the appropriate loader based on the file extension.
    filename = Path(filename)
    if filename.suffix.lower() == ".mtx":
        return load_mtx(filename)
    graph = None
    expected_edges = None
    
    # It reads DIMACS header and edges, skipping comments.
    with open(filename, "r", encoding="utf-8") as f:
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
                
    # The code verifies that the graph was loaded with the expected edge count.
    if graph is None or len(graph.edges) != expected_edges:
        raise ValueError("Missing header or incorrect edge count")
    return graph
