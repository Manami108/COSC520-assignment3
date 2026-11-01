"""Basic checks for algorithms and dataset loading.

Run: python -m unittest tests.tests -v
"""

import unittest

from algorithms.graph_coloring import (
    basic_graph_coloring, dsatur_coloring, valid_coloring,
)
from algorithms.vertex_cover import (
    basic_vertex_cover, randomized_vertex_cover, valid_vertex_cover,
)
from experiments.dataset import Graph, load_graph


class AlgorithmTests(unittest.TestCase):
    def test_basic_vertex_cover(self):
        """Check that the basic method selects both ends of one edge."""
        graph = Graph(2)
        graph.add_edge(0, 1)
        self.assertEqual(basic_vertex_cover(graph), {0, 1})

    def test_randomized_vertex_cover(self):
        """Check both covers on a graph with several edges."""
        graph = load_graph("data/example.col")
        self.assertTrue(valid_vertex_cover(graph, basic_vertex_cover(graph)))
        self.assertTrue(valid_vertex_cover(graph, randomized_vertex_cover(graph, seed=7)))

    def test_graph_coloring(self):
        """Check that both colorings are valid on a triangle."""
        graph = Graph(3)
        for edge in [(0, 1), (1, 2), (0, 2)]:
            graph.add_edge(*edge)
        for coloring in (basic_graph_coloring, dsatur_coloring):
            colors = coloring(graph)
            self.assertTrue(valid_coloring(graph, colors))
            self.assertEqual(len(set(colors)), 3)

    def test_dsatur_on_crown_graph(self):
        """Check that DSATUR uses two colors on an interleaved crown graph."""
        graph = Graph(8)
        for i in range(4):
            for j in range(4):
                if i != j:
                    graph.add_edge(2 * i, 2 * j + 1)
        colors = dsatur_coloring(graph)
        self.assertTrue(valid_coloring(graph, colors))
        self.assertEqual(len(set(colors)), 2)

    def test_empty_graph(self):
        """Check that isolated vertices do not cause an error."""
        graph = Graph(4)
        self.assertEqual(basic_vertex_cover(graph), set())
        self.assertEqual(basic_graph_coloring(graph), [0, 0, 0, 0])

    def test_dataset(self):
        """Check that the DIMACS file loads with correct graph dimensions."""
        graph = load_graph("data/example.col")
        self.assertEqual((graph.n, len(graph.edges)), (6, 6))

    def test_duplicate_edges(self):
        """Adding the same undirected edge twice must not duplicate it."""
        graph = Graph(2)
        graph.add_edge(0, 1)
        graph.add_edge(1, 0)
        self.assertEqual(graph.edges, [(0, 1)])


if __name__ == "__main__":
    unittest.main()
