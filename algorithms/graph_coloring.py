"""Basic greedy and DSATUR graph coloring algorithms."""


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


def dsatur_coloring(graph):
    """Input: graph. Output: DSATUR coloring.

    Choose the vertex with the most different colored neighbors.
    Break ties by higher degree, then lower vertex number.
    """
    colors = [-1] * graph.n
    uncolored = set(range(graph.n))
    neighbor_colors = [set() for _ in range(graph.n)]

    while uncolored:
        u = max(uncolored, key=lambda v:
                (len(neighbor_colors[v]), len(graph.adj[v]), -v))

        color = 0
        while color in neighbor_colors[u]:
            color += 1
        colors[u] = color
        uncolored.remove(u)

        for v in graph.adj[u]:
            if v in uncolored:
                neighbor_colors[v].add(color)

    return colors


def valid_coloring(graph, colors):
    """Input: graph and colors. Output: whether all adjacent colors differ."""
    return (len(colors) == graph.n
            and all(isinstance(c, int) and c >= 0 for c in colors)
            and all(colors[u] != colors[v] for u, v in graph.edges))


def number_of_colors(colors):
    """Input: color list. Output: count of distinct colors."""
    return len(set(colors))
