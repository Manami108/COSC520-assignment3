# Vertex Cover is a set of vertices such that every edge has at least one endpoint in the set.
# The basic algorithm adds both endpoints of each uncovered edge, and the randomized version selects one random endpoint of each uncovered edge
import random

def basic_vertex_cover(graph):
    # Input: graph
    # Output: set of vertices covering every edge
    # The code adds both endpoints of each uncovered edge.
    cover = set()
    for u, v in graph.edges:
        if u not in cover and v not in cover:
            cover.add(u)
            cover.add(v)
    return cover


def randomized_vertex_cover(graph, seed=42):
    # Input: graph and seed
    # Output: a randomized vertex cover
    # In contrast to the previous code block, this code randomly selects one endpoint of each uncovered edge
    rng = random.Random(seed)
    cover = set()
    for u, v in graph.edges:
        if u not in cover and v not in cover:
            cover.add(rng.choice((u, v)))
    return cover


def valid_vertex_cover(graph, cover):
    # Input: graph and selected vertices
    # Output: whether all edges are covered
    # Each edge must satisfy u in cover or v in cover
    return all(u in cover or v in cover for u, v in graph.edges)
