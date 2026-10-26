"""Small demonstration of the four algorithms."""

from algorithms.graph_coloring import basic_graph_coloring, degree_ordered_coloring
from algorithms.vertex_cover import basic_vertex_cover, randomized_vertex_cover
from experiments.dataset import load_graph


def main():
    """Input: none. Output: algorithm solutions for the example graph."""
    graph = load_graph("data/example.col")
    print(f"Example graph: {graph.n} vertices, {len(graph.edges)} edges")
    print("Basic cover:", sorted(basic_vertex_cover(graph)))
    print("Randomized cover:", sorted(randomized_vertex_cover(graph, seed=42)))
    print("Basic coloring:", basic_graph_coloring(graph))
    print("Degree-ordered coloring:", degree_ordered_coloring(graph))


if __name__ == "__main__":
    main()
