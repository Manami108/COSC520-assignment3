# This is unit tests for algorithm correctness and graph data loading.
import tempfile
from pathlib import Path
import unittest
from algorithms.graph_coloring import (basic_graph_coloring, dsatur_coloring, valid_coloring,)
from algorithms.vertex_cover import (basic_vertex_cover, randomized_vertex_cover, valid_vertex_cover,)
from experiments.dataset import Graph, load_graph

class AlgorithmTests(unittest.TestCase):
    def test_basic_vertex_cover(self):
        # This code checks that the basic method selects both ends of one edge.
        graph = Graph(2)
        graph.add_edge(0, 1)
        self.assertEqual(basic_vertex_cover(graph), {0, 1})

    def test_randomized_vertex_cover(self):
        # This code checks both covers on a graph with several edges.
        graph = load_graph("data/example.col")
        self.assertTrue(valid_vertex_cover(graph, basic_vertex_cover(graph)))
        self.assertTrue(valid_vertex_cover(graph, randomized_vertex_cover(graph, seed=7)))

    def test_graph_coloring(self):
        # This code checks that both colorings are valid on a triangle.
        graph = Graph(3)
        for edge in [(0, 1), (1, 2), (0, 2)]:
            graph.add_edge(*edge)
        for coloring in (basic_graph_coloring, dsatur_coloring):
            colors = coloring(graph)
            self.assertTrue(valid_coloring(graph, colors))
            self.assertEqual(len(set(colors)), 3)

    def test_dsatur_on_crown_graph(self):
        # This code checks that DSATUR uses two colors on an interleaved crown graph.
        # The edges connect vertices 2*i and 2*j+1 only when i != j.
        graph = Graph(8)
        for i in range(4):
            for j in range(4):
                if i != j:
                    graph.add_edge(2 * i, 2 * j + 1)
        colors = dsatur_coloring(graph)
        self.assertTrue(valid_coloring(graph, colors))
        self.assertEqual(len(set(colors)), 2)

    def test_empty_graph(self):
        # This code checks that isolated vertices do not cause an error.
        graph = Graph(4)
        self.assertEqual(basic_vertex_cover(graph), set())
        self.assertEqual(basic_graph_coloring(graph), [0, 0, 0, 0])

    def test_dataset(self):
        # This code checks that the DIMACS file loads with correct graph dimensions.
        graph = load_graph("data/example.col")
        self.assertEqual((graph.n, len(graph.edges)), (6, 6))

    def test_duplicate_edges(self):
        # This code checks that adding the same undirected edge twice does not create duplicates.
        graph = Graph(2)
        graph.add_edge(0, 1)
        graph.add_edge(1, 0)
        self.assertEqual(graph.edges, [(0, 1)])
    
    def test_matrix_market_loader(self):
        # This code checks that Matrix Market entries are loaded as undirected edges.
        with tempfile.TemporaryDirectory() as directory:
            filename = Path(directory) / "small.mtx"
            filename.write_text(
                "%%MatrixMarket matrix coordinate pattern symmetric\n"
                "% Sample graph\n"
                "4 4 3\n"
                "1 2\n"
                "2 3\n"
                "3 4\n",
                encoding="utf-8",)

            graph = load_graph(filename)
        self.assertEqual(graph.n, 4)
        self.assertEqual(len(graph.edges), 3)
        self.assertEqual(set(graph.edges), {(0, 1), (1, 2), (2, 3)})
        self.assertEqual(graph.adj[1], {0, 2})

if __name__ == "__main__":
    unittest.main()
