"""Runnable examples for Prim, Kruskal (DSU), and Ford-Fulkerson.

Run in PyCharm with:  python graph_algorithms.py
All graphs are represented with plain Python dictionaries/lists.
"""

from collections import defaultdict, deque
from heapq import heappop, heappush


def prim_mst(graph, start=None):
    """Return (MST edges, total weight). Raises ValueError if disconnected."""
    if not graph:
        return [], 0
    start = start if start is not None else next(iter(graph))
    visited = {start}
    heap = []
    for neighbor, weight in graph[start]:
        heappush(heap, (weight, start, neighbor))

    mst, total = [], 0
    while heap and len(visited) < len(graph):
        weight, source, target = heappop(heap)
        if target in visited:
            continue
        visited.add(target)
        mst.append((source, target, weight))
        total += weight
        for neighbor, next_weight in graph[target]:
            if neighbor not in visited:
                heappush(heap, (next_weight, target, neighbor))

    if len(visited) != len(graph):
        raise ValueError("Prim requires a connected graph; use a forest for disconnected input.")
    return mst, total


class DisjointSet:
    """Union-find with path compression and union by rank."""

    def __init__(self, vertices):
        self.parent = {vertex: vertex for vertex in vertices}
        self.rank = {vertex: 0 for vertex in vertices}

    def find(self, vertex):
        if self.parent[vertex] != vertex:
            self.parent[vertex] = self.find(self.parent[vertex])
        return self.parent[vertex]

    def union(self, first, second):
        root_a, root_b = self.find(first), self.find(second)
        if root_a == root_b:
            return False
        if self.rank[root_a] < self.rank[root_b]:
            root_a, root_b = root_b, root_a
        self.parent[root_b] = root_a
        if self.rank[root_a] == self.rank[root_b]:
            self.rank[root_a] += 1
        return True


def kruskal_msf(vertices, edges):
    """Return a minimum spanning forest as (edges, total weight)."""
    sets = DisjointSet(vertices)
    forest, total = [], 0
    for source, target, weight in sorted(edges, key=lambda edge: edge[2]):
        if sets.union(source, target):
            forest.append((source, target, weight))
            total += weight
    return forest, total


def ford_fulkerson(capacity, source, sink):
    """Return (maximum flow value, flow dictionary) using BFS augmenting paths.

    BFS makes this the Edmonds-Karp path-selection version of Ford-Fulkerson.
    """
    vertices = set(capacity)
    for neighbors in capacity.values():
        vertices.update(neighbors)

    residual = {u: defaultdict(int) for u in vertices}
    flow = {u: defaultdict(int) for u in vertices}
    adjacency = {u: set() for u in vertices}
    for u, neighbors in capacity.items():
        for v, amount in neighbors.items():
            if amount < 0:
                raise ValueError("Capacities must be nonnegative.")
            residual[u][v] = amount
            adjacency[u].add(v)
            adjacency[v].add(u)

    maximum = 0
    while True:
        parent = {source: None}
        queue = deque([source])
        while queue and sink not in parent:
            u = queue.popleft()
            for v in adjacency[u]:
                if v not in parent and residual[u][v] > 0:
                    parent[v] = u
                    queue.append(v)
        if sink not in parent:
            break

        amount = float("inf")
        v = sink
        while v != source:
            u = parent[v]
            amount = min(amount, residual[u][v])
            v = u

        v = sink
        while v != source:
            u = parent[v]
            residual[u][v] -= amount
            residual[v][u] += amount
            flow[u][v] += amount
            flow[v][u] -= amount
            v = u
        maximum += amount

    readable_flow = {
        u: {v: amount for v, amount in neighbors.items() if amount > 0}
        for u, neighbors in flow.items()
    }
    return maximum, readable_flow


def undirected_graph(edges):
    graph = defaultdict(list)
    for source, target, weight in edges:
        graph[source].append((target, weight))
        graph[target].append((source, weight))
    return dict(graph)


if __name__ == "__main__":
    weighted_edges = [
        ("A", "B", 1), ("A", "C", 4), ("B", "C", 2),
        ("B", "D", 5), ("C", "D", 1), ("D", "E", 3),
    ]
    vertices = {vertex for edge in weighted_edges for vertex in edge[:2]}
    print("Prim:", prim_mst(undirected_graph(weighted_edges), "A"))
    print("Kruskal:", kruskal_msf(vertices, weighted_edges))

    network = {
        "s": {"a": 3, "b": 2},
        "a": {"b": 1, "t": 2},
        "b": {"t": 3},
        "t": {},
    }
    print("Ford-Fulkerson:", ford_fulkerson(network, "s", "t"))
