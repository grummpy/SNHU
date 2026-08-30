"""CS 508 Module Eight: weighted graphs, BFS, Dijkstra, and Bellman-Ford.

Run with:
    python3 cs508_graph_algorithms.py

Assumptions:
* Every traversal and shortest-path calculation starts at vertex 1.
* BFS visits adjacent vertices in ascending numeric order.
* Graph 1 is undirected.
* Graph 2 is directed, following the arrowheads in the original diagram.
"""

from collections import deque
from math import inf
from typing import Dict, Iterable, List, Optional, Tuple


Edge = Tuple[int, int, float]


GRAPH_1_VERTICES = list(range(1, 8))
GRAPH_1_EDGES: List[Edge] = [
    (1, 2, 4),
    (1, 3, 2),
    (2, 4, 5),
    (2, 5, 10),
    (3, 6, 3),
    (4, 5, 2),
    (5, 6, 8),
    (5, 7, 6),
    (6, 7, 1),
]

GRAPH_2_VERTICES = list(range(1, 6))
GRAPH_2_EDGES: List[Edge] = [
    (1, 2, 5),
    (1, 3, 3),
    (2, 4, 2),
    (3, 4, 6),
    (3, 5, 4),
    (4, 5, 7),
]


def build_adjacency_list(
    vertices: Iterable[int], edges: Iterable[Edge], directed: bool
) -> Dict[int, List[Tuple[int, float]]]:
    """Return a sorted weighted adjacency list."""
    adjacency = {vertex: [] for vertex in vertices}
    for source, target, weight in edges:
        adjacency[source].append((target, weight))
        if not directed:
            adjacency[target].append((source, weight))
    for neighbors in adjacency.values():
        neighbors.sort(key=lambda item: item[0])
    return adjacency


def build_weighted_matrix(
    vertices: List[int], edges: Iterable[Edge], directed: bool
) -> List[List[float]]:
    """Build a weighted adjacency matrix; infinity denotes no direct edge."""
    index = {vertex: position for position, vertex in enumerate(vertices)}
    matrix = [[inf] * len(vertices) for _ in vertices]
    for i in range(len(vertices)):
        matrix[i][i] = 0
    for source, target, weight in edges:
        matrix[index[source]][index[target]] = weight
        if not directed:
            matrix[index[target]][index[source]] = weight
    return matrix


def bfs(
    adjacency: Dict[int, List[Tuple[int, float]]], start: int
) -> List[int]:
    """Return BFS discovery order. Edge weights do not affect BFS."""
    visited = {start}
    order = []
    queue = deque([start])
    while queue:
        vertex = queue.popleft()
        order.append(vertex)
        for neighbor, _ in adjacency[vertex]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
    return order


def dijkstra(
    adjacency: Dict[int, List[Tuple[int, float]]], start: int
) -> Tuple[Dict[int, float], Dict[int, Optional[int]]]:
    """Return shortest distances and predecessors for nonnegative weights."""
    import heapq

    distances = {vertex: inf for vertex in adjacency}
    previous: Dict[int, Optional[int]] = {vertex: None for vertex in adjacency}
    distances[start] = 0
    queue = [(0, start)]

    while queue:
        current_distance, vertex = heapq.heappop(queue)
        if current_distance != distances[vertex]:
            continue
        for neighbor, weight in adjacency[vertex]:
            candidate = current_distance + weight
            if candidate < distances[neighbor]:
                distances[neighbor] = candidate
                previous[neighbor] = vertex
                heapq.heappush(queue, (candidate, neighbor))
    return distances, previous


def bellman_ford(
    vertices: List[int], edges: List[Edge], start: int, directed: bool
) -> Tuple[Dict[int, float], Dict[int, Optional[int]]]:
    """Return shortest distances and predecessors; detect negative cycles."""
    relaxation_edges = list(edges)
    if not directed:
        relaxation_edges += [(target, source, weight) for source, target, weight in edges]

    distances = {vertex: inf for vertex in vertices}
    previous: Dict[int, Optional[int]] = {vertex: None for vertex in vertices}
    distances[start] = 0

    for _ in range(len(vertices) - 1):
        changed = False
        for source, target, weight in relaxation_edges:
            if distances[source] != inf and distances[source] + weight < distances[target]:
                distances[target] = distances[source] + weight
                previous[target] = source
                changed = True
        if not changed:
            break

    for source, target, weight in relaxation_edges:
        if distances[source] != inf and distances[source] + weight < distances[target]:
            raise ValueError("Graph contains a reachable negative-weight cycle")
    return distances, previous


def reconstruct_path(
    previous: Dict[int, Optional[int]], start: int, target: int
) -> List[int]:
    """Reconstruct one shortest path from a predecessor mapping."""
    path = []
    current: Optional[int] = target
    while current is not None:
        path.append(current)
        if current == start:
            return list(reversed(path))
        current = previous[current]
    return []


def format_number(value: float) -> str:
    if value == inf:
        return "INF"
    numeric = float(value)
    return str(int(numeric)) if numeric.is_integer() else f"{numeric:g}"


def print_matrix(vertices: List[int], matrix: List[List[float]]) -> None:
    print("      " + "".join(f"{vertex:>6}" for vertex in vertices))
    for vertex, row in zip(vertices, matrix):
        print(f"{vertex:>4}  " + "".join(f"{format_number(value):>6}" for value in row))


def print_shortest_paths(
    title: str,
    vertices: List[int],
    distances: Dict[int, float],
    previous: Dict[int, Optional[int]],
    start: int,
) -> None:
    print(title)
    for target in vertices:
        path = reconstruct_path(previous, start, target)
        path_text = " -> ".join(map(str, path)) if path else "unreachable"
        print(f"  1 to {target}: distance={format_number(distances[target])}, path={path_text}")


def analyze_graph(
    name: str, vertices: List[int], edges: List[Edge], directed: bool
) -> None:
    adjacency = build_adjacency_list(vertices, edges, directed)
    matrix = build_weighted_matrix(vertices, edges, directed)
    bfs_order = bfs(adjacency, 1)
    dijkstra_distances, dijkstra_previous = dijkstra(adjacency, 1)
    bellman_distances, bellman_previous = bellman_ford(vertices, edges, 1, directed)

    print(f"\n{'=' * 72}\n{name} ({'directed' if directed else 'undirected'})\n{'=' * 72}")
    print("\nWeighted adjacency matrix (INF = no direct edge):")
    print_matrix(vertices, matrix)
    print(f"\nBFS order from vertex 1: {' -> '.join(map(str, bfs_order))}\n")
    print_shortest_paths("Dijkstra results from vertex 1:", vertices, dijkstra_distances, dijkstra_previous, 1)
    print()
    print_shortest_paths("Bellman-Ford results from vertex 1:", vertices, bellman_distances, bellman_previous, 1)

    assert dijkstra_distances == bellman_distances


def main() -> None:
    analyze_graph("Graph 1", GRAPH_1_VERTICES, GRAPH_1_EDGES, directed=False)
    analyze_graph("Graph 2", GRAPH_2_VERTICES, GRAPH_2_EDGES, directed=True)


if __name__ == "__main__":
    main()
