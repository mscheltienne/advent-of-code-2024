from __future__ import annotations

from itertools import product
from pathlib import Path
from typing import TYPE_CHECKING

import networkx as nx
import numpy as np

if TYPE_CHECKING:
    from numpy.typing import NDArray

fname: Path = Path(__file__).parent / "input.txt"
char_to_num: dict[str, int] = dict()
with open(fname) as fid:
    data: list[str] = [line.strip() for line in fid.readlines()]
data_numerical: list[list[int]] = []
for line in data:
    new_char = set(line).difference(set(char_to_num))
    for char in new_char:
        char_to_num[char] = len(char_to_num)
    line = [char_to_num[char] for char in line]
    data_numerical.append(line)
data: NDArray[np.int8] = np.array(data_numerical, dtype=np.int8)
num_to_char: dict[int, str] = {v: k for k, v in char_to_num.items()}


# %% part 1
def build_graph() -> nx.Graph:
    """Build a graph representation of the map."""
    G = nx.Graph()
    rows, cols = data.shape
    for x, y in product(range(rows), range(cols)):
        G.add_node((x, y))
        for dx, dy in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
            new_x, new_y = x + dx, y + dy
            if in_bounds(data, new_x, new_y) and data[new_x, new_y] == data[x, y]:
                G.add_edge((x, y), (new_x, new_y))
    return G


def in_bounds(data: NDArray[np.int8], x: int, y: int) -> bool:
    """Check if the antinode is still on the map."""
    rows, cols = data.shape
    return 0 <= x < rows and 0 <= y < cols


def estimate_fence_cost(G: nx.Graph) -> int:
    """Estimate the cost of the fence."""
    return sum(
        len(elt) * sum(4 - G.degree[node] for node in elt)
        for elt in nx.connected_components(G)
    )


G = build_graph()
total = estimate_fence_cost(G)
print(f"The cost of the fence is {total}.")


# %% part 2
def build_boundary_graph(
    component: set[tuple[int, int]],
) -> nx.Graph:
    """Find the boundary edges of a component."""
    G_boundary = nx.Graph()
    for x, y in component:
        for dx, dy in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
            new_x, new_y = x + dx, y + dy
            if in_bounds(data, new_x, new_y) and (new_x, new_y) in component:
                continue  # the new point is within the same region
            # this is a boundary edge between (x, y) and (new_x, new_y), let's add it in
            # our grid-representation of the boundaries.
            if dx == -1 and dy == 0:  # edge on the top of (x, y)
                p1 = (x, y)
                p2 = (x, y + 1)
            elif dx == 1 and dy == 0:  # edge on the bottom of (x, y)
                p1 = (x + 1, y)
                p2 = (x + 1, y + 1)
            elif dx == 0 and dy == -1:  # edge on the left of (x, y)
                p1 = (x, y)
                p2 = (x + 1, y)
            elif dx == 0 and dy == 1:  # edge on the right of (x, y)
                p1 = (x, y + 1)
                p2 = (x + 1, y + 1)
            G_boundary.add_edge(p1, p2)
    return G_boundary


def count_sides(component: set[tuple[int, int]]) -> int:
    """Count the number of cycles of the component."""
    G_boundary = build_boundary_graph(component)
    cycles = nx.cycle_basis(G_boundary)  # find all cycles within the component
    n_sides = 0
    for cycle in cycles:
        G_boundary_sub = G_boundary.subgraph(cycle)
        n_sides += count_cycle_sides(G_boundary_sub)
    return n_sides


def count_cycle_sides(G_boundary: nx.Graph) -> int:
    """Count the number of sides of the cycle.

    The graph G_boundary has exactly 1 cycle, i..e. each node has 2 edges.
    """
    start = next(iter(G_boundary.nodes))
    n_sides = _init_n_sides(G_boundary, start)
    pos = start
    prev_pos = None
    while True:
        neighbors = list(G_boundary[pos])
        assert len(neighbors) == 2  # sanity-check
        if prev_pos is None:
            next_pos = neighbors[0]
        else:
            next_pos = neighbors[0] if neighbors[1] == prev_pos else neighbors[1]
        if prev_pos is not None and get_direction(prev_pos, pos) != get_direction(
            pos, next_pos
        ):
            n_sides += 1
        if next_pos == start:
            break
        prev_pos, pos = pos, next_pos
    return n_sides


def _init_n_sides(G_boundary: nx.Graph, pos: tuple[int, int]) -> int:
    """Initialize n_sides to 0 if we start on a 'line', and 1 if in a 'corner'."""
    neighbors = list(G_boundary[pos])
    assert len(neighbors) == 2  # sanity-check
    if get_direction(pos, neighbors[0]) == get_direction(pos, neighbors[1]):
        return 0
    return 1


def get_direction(p1: tuple[int, int], p2: tuple[int, int]) -> str:
    """Get the direction from p1 to p2."""
    if p1[0] == p2[0]:
        return "horizontal"
    elif p1[1] == p2[1]:
        return "vertical"


def estimate_fence_cost(G: nx.Graph) -> int:
    """Estimate the cost of the fence."""
    return sum(len(elt) * count_sides(elt) for elt in nx.connected_components(G))


G = build_graph()
total = estimate_fence_cost(G)
print(f"The cost of the fence is {total}.")
