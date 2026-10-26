"""Greedy graph coloring using two different vertex orderings."""


def greedy_coloring(graph, order):
    """Input: graph and vertex order. Output: color index for each vertex.

    Give each vertex the smallest color not used by its colored neighbors.
    """
    colors = [-1] * graph.n
    for u in order:
        neighbor_colors = {colors[v] for v in graph.adj[u] if colors[v] != -1}
        color = 0
        while color in neighbor_colors:
            color += 1
        colors[u] = color
    return colors


def basic_graph_coloring(graph):
    """Input: graph. Output: greedy coloring in vertex-number order."""
    return greedy_coloring(graph, range(graph.n))


def degree_ordered_coloring(graph):
    """Input: graph. Output: coloring with highest-degree vertices first.

    For equal degrees, the vertex with the smaller number comes first.
    """
    order = sorted(range(graph.n), key=lambda u: (-len(graph.adj[u]), u))
    return greedy_coloring(graph, order)


def valid_coloring(graph, colors):
    """Input: graph and colors. Output: whether all adjacent colors differ."""
    return (len(colors) == graph.n
            and all(isinstance(c, int) and c >= 0 for c in colors)
            and all(colors[u] != colors[v] for u, v in graph.edges))


def number_of_colors(colors):
    """Input: color list. Output: count of distinct colors."""
    return len(set(colors))
