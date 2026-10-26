"""Basic and randomized vertex cover algorithms."""

import random


def basic_vertex_cover(graph):
    """Input: graph. Output: set of vertices covering every edge.

    Choose both endpoints of each edge that is still uncovered.
    """
    cover = set()
    for u, v in graph.edges:
        if u not in cover and v not in cover:
            cover.add(u)
            cover.add(v)
    return cover


def randomized_vertex_cover(graph, seed=42):
    """Input: graph and seed. Output: a randomized vertex cover.

    Choose one random endpoint of each uncovered edge.
    """
    rng = random.Random(seed)
    cover = set()
    for u, v in graph.edges:
        if u not in cover and v not in cover:
            cover.add(rng.choice((u, v)))
    return cover


def valid_vertex_cover(graph, cover):
    """Input: graph and selected vertices. Output: whether all edges are covered."""
    return all(u in cover or v in cover for u, v in graph.edges)
